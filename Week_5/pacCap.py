import pyshark

# Capture a few HTTP or DNS packets; adjust interface
cap = pyshark.LiveCapture(interface="eth0", bpf_filter="port 53 or port 80")
cap.sniff(timeout=10)  # 10 seconds

print(f"Captured: {len(cap)} packets")
for pkt in cap[:10]:
    layers = [l.layer_name for l in pkt.layers]
    print("Layers:", layers)
    if "dns" in layers:
        print(" DNS query:", getattr(pkt.dns, "qry_name", ""))
    if "http" in layers:
        print(" HTTP host:", getattr(pkt.http, "host", ""))
