# Air-gapped replay instructions (high level)

1. Create an isolated network namespace or physical air-gapped lab with one client and one server.
2. Run a browser in the client, capture the TLS handshake with tcpdump.
3. Use Wireshark to export the ClientHello as structured JSON. Feed that JSON into `analysis_cli`.
4. If you must replay traffic for testing, use a controlled server under your ownership and ensure no external connectivity.
