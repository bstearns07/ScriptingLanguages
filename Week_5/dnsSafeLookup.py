"""
DNS Queries & Defense (dnspython + allow-lists)

Usage (examples):
    python dns_safe_lookup.py example.com A
    python dns_safe_lookup.py wsc.edu MX
"""

import sys
import re
import time
import idna
import dns.resolver
import dns.exception
from typing import List, Optional

# ----------------------------
# 1) Policy knobs (tune in class)
# ----------------------------

# Pin resolvers you trust (allow-list of DNS servers).
# You can add your campus recursive resolvers here.
PINNED_NAMESERVERS = ["1.1.1.1", "9.9.9.9"]  # Cloudflare, Quad9

# Optional: allow only these record types
ALLOWED_TYPES = {"A", "AAAA", "MX", "TXT", "NS", "CNAME"}

# Optional: restrict to zones you expect in class (comment out to disable)
OPTIONAL_ALLOWED_SUFFIXES = [
    # ".wsc.edu",             # example: allow only school domains
    # ".example.com",
]

# Query limits
DEFAULT_TIMEOUT = 2.0  # seconds per try
MAX_RETRIES = 2  # total tries = 1 + MAX_RETRIES
MAX_CNAME_DEPTH = 5
MAX_DOMAIN_LENGTH = 253
MAX_LABEL_LENGTH = 63

# Strict domain pattern: labels of letters/digits/hyphen, proper dots, TLD >= 2
DOMAIN_RE = re.compile(
    r"^(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
)


# ----------------------------
# 2) Helpers: normalize & validate
# ----------------------------

def normalize_domain(name: str) -> str:
    """
    Normalize a potentially Unicode domain to ASCII (punycode) and strip spaces.
    """
    name = name.strip().rstrip(".")  # drop trailing dot; we’ll query absolute
    if not name:
        return name
    try:
        # Convert each label with IDNA
        labels = name.split(".")
        ascii_labels = [idna.encode(lbl).decode("ascii") for lbl in labels]
        return ".".join(ascii_labels)
    except Exception:
        # If IDNA fails, return something invalid to trigger validation failure
        return ""


def is_valid_domain(name: str) -> bool:
    """
    Validate domain using length rules and regex. Assumes ASCII/punycode.
    """
    if not name:
        return False
    if len(name) > MAX_DOMAIN_LENGTH:
        return False
    labels = name.split(".")
    if any(len(lbl) == 0 or len(lbl) > MAX_LABEL_LENGTH for lbl in labels):
        return False
    # Require at least 2 labels and TLD alpha
    if not DOMAIN_RE.match(name):
        return False
    return True


def is_allowed_suffix(name: str) -> bool:
    """
    If OPTIONAL_ALLOWED_SUFFIXES configured, ensure name ends with one of them.
    Disabled if list is empty.
    """
    if not OPTIONAL_ALLOWED_SUFFIXES:
        return True
    name_lc = name.lower()
    return any(name_lc.endswith(sfx.lower()) for sfx in OPTIONAL_ALLOWED_SUFFIXES)


# ----------------------------
# 3) Safe resolver wrapper
# ----------------------------

class SafeResolver:
    """
    Resolver pinned to an allow-list of nameservers with bounded timeouts and retries.
    """

    def __init__(self,
                 nameservers: List[str],
                 timeout: float = DEFAULT_TIMEOUT,
                 retries: int = MAX_RETRIES):
        if not nameservers:
            raise ValueError("At least one nameserver must be provided.")
        self.resolver = dns.resolver.Resolver(configure=False)
        self.resolver.nameservers = nameservers
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout  # total per-try
        # dnspython internally handles some retry logic; we'll layer a simple loop too
        self.retries = max(0, retries)

    def resolve_once(self, qname: str, rtype: str):
        return self.resolver.resolve(qname, rtype, raise_on_no_answer=True)

    def resolve(self, qname: str, rtype: str):
        """
        Resolve with bounded retries and small exponential backoff.
        """
        last_exc = None
        for attempt in range(self.retries + 1):
            try:
                return self.resolve_once(qname, rtype)
            except (dns.resolver.NXDOMAIN,
                    dns.resolver.NoAnswer,
                    dns.resolver.NoNameservers) as e:
                # Terminal-ish conditions for our use-case: don't keep retrying much
                last_exc = e
                if attempt == self.retries:
                    raise
                time.sleep(0.1 * (2 ** attempt))
            except (dns.exception.Timeout, OSError) as e:
                last_exc = e
                if attempt == self.retries:
                    raise
                time.sleep(0.1 * (2 ** attempt))
            except Exception as e:
                # Unexpected—don’t spin forever
                last_exc = e
                raise
        if last_exc:
            raise last_exc


# ----------------------------
# 4) High-level safe query
# ----------------------------

def safe_query(domain: str, rtype: str, resolver: Optional[SafeResolver] = None) -> List[str]:
    """
    Safely resolve a domain with defenses:
    - Normalize to punycode, validate syntax and length constraints.
    - Enforce optional suffix allow-list.
    - Enforce record-type allow-list.
    - Pin to selected nameservers.
    - Limit CNAME depth by re-querying the final target (sanity check).
    - Return stringified rdata items (IPs, hosts, etc.).
    """
    if resolver is None:
        resolver = SafeResolver(PINNED_NAMESERVERS)

    # Normalize + validate
    qname = normalize_domain(domain)
    if not is_valid_domain(qname):
        raise ValueError("Invalid domain format after normalization (IDNA/punycode).")
    if not is_allowed_suffix(qname):
        raise PermissionError("Domain is not in allowed suffix list.")

    rtype = rtype.upper().strip()
    if rtype not in ALLOWED_TYPES:
        raise PermissionError(f"Record type '{rtype}' is not allowed (policy).")

    # Primary resolve
    answers = resolver.resolve(qname, rtype)

    # Basic owner-name sanity check: the RRset name should match qname (or be an allowed CNAME target)
    owner = str(answers.rrset.name).rstrip(".")
    # dnspython may chase CNAMEs internally for types other than CNAME. We can bound depth by re-walking if needed.
    if rtype != "CNAME" and owner.lower() != qname.lower():
        # If the owner is different (due to CNAME), do a manual bounded CNAME walk
        target = _follow_cname_chain(qname, resolver)
        # Optionally re-resolve final canonical name for requested type:
        answers = resolver.resolve(target, rtype)
        owner = str(answers.rrset.name).rstrip(".")
        if owner.lower() != target.lower():
            raise RuntimeError("Owner name mismatch after CNAME resolution.")

    # Stringify RDATA
    out = []
    for rdata in answers:
        out.append(str(rdata))
    return out


def _follow_cname_chain(name: str, resolver: SafeResolver) -> str:
    """
    Follow CNAME up to MAX_CNAME_DEPTH and return the final canonical name.
    """
    current = name
    for _ in range(MAX_CNAME_DEPTH):
        try:
            ans = resolver.resolve(current, "CNAME")
            # If there is a CNAME, move to its target (rdata.target is a dns.name.Name)
            target = str(ans[0].target).rstrip(".")
            current = target
        except dns.resolver.NoAnswer:
            # No CNAME; current is canonical
            return current
    raise RuntimeError("CNAME chain too deep; possible loop or misconfig.")


# ----------------------------
# 5) CLI entrypoint for class demos
# ----------------------------

def main(argv: List[str]) -> int:
    if len(argv) < 3:
        print("Usage: python dns_safe_lookup.py <domain> <rtype>")
        print("Example: python dns_safe_lookup.py example.com A")
        return 2

    domain = argv[1]
    rtype = argv[2].upper()

    try:
        resolver = SafeResolver(PINNED_NAMESERVERS, timeout=DEFAULT_TIMEOUT, retries=MAX_RETRIES)
        answers = safe_query(domain, rtype, resolver=resolver)
        print(f"{domain} {rtype} answers:")
        for i, item in enumerate(answers, 1):
            print(f"  {i}. {item}")
        return 0
    except (ValueError, PermissionError) as e:
        print(f"[POLICY] {e}")
        return 1
    except dns.resolver.NXDOMAIN:
        print("[DNS] NXDOMAIN: domain does not exist.")
        return 1
    except dns.resolver.NoAnswer:
        print("[DNS] NoAnswer: no records of that type.")
        return 1
    except dns.exception.Timeout:
        print("[DNS] Timeout: resolver took too long.")
        return 1
    except dns.resolver.NoNameservers:
        print("[DNS] NoNameservers: all pinned resolvers failed.")
        return 1
    except Exception as e:
        print(f"[ERR] {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
