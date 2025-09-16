import re
import dns.resolver

# maps to a dns domain address entry
domain_pattern = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$")

# Use a known recursive resolver (Cloudflare)
safe_resolver = dns.resolver.Resolver()
safe_resolver.nameservers = ["1.1.1.1"]

def query_records(name: str, rtype: str = "A"):
    if not domain_pattern.match(name):
        raise ValueError("Invalid domain format")
    answers = safe_resolver.resolve(name, rtype, lifetime=3.0)
    return [str(rdata) for rdata in answers]

if __name__ == "__main__":
    for r in ["A", "AAAA", "MX"]:
        try:
            print(r, query_records("wsc.edu", r))
        except Exception as e:
            print("ERR:", e)
