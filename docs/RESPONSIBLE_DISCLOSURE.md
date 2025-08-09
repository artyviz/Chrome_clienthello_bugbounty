# Responsible Disclosure & Lab Guidance

Use this toolkit only for defensive testing, research, or authorized bug-bounty submissions.

## Safe capture guidance
- Capture traffic only from systems you own and control.
- Use `tcpdump`/`tshark` to capture traffic and export ClientHello details using Wireshark's `Export Packet Dissections` -> JSON option.
- Do not replay or transmit captured ClientHello bytes to third-party servers.

## Air-gapped replay
- To reproduce detection behavior locally, set up an isolated network with a controlled server and client.
- Use the tools here to analyze the captured ClientHello from your local browser instance.

## Disclosure
Include in your bounty submission: PCAPs captured locally, analysis report (JSON output), recommended mitigations, and steps to reproduce in an air-gapped environment.
