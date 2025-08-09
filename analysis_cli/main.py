# CLI entrypoint for ClientHello analysis.
import argparse, json, os, subprocess, shutil, sys
from .ja3 import ja3_from_fields, ja3_hash, ja4_from_fields
from .tshark_parser import parse_tshark_json

def load_json(path):
    with open(path,'r') as f:
        return json.load(f)

def extract_clienthello_from_tshark(pcap_path, out_json_path):
    # This is a helper that attempts to use `tshark` to extract TLS ClientHello fields.
    # It is safe: it only reads local pcap and writes a JSON file. If tshark isn't available,
    # the CLI falls back to requiring a structured JSON input.
    if not shutil.which('tshark'):
        raise RuntimeError('tshark not found in PATH; please export ClientHello as JSON via Wireshark/tshark or provide structured JSON input.')
    # Example tshark command (may need adjustment per tshark version)
    cmd = ['tshark','-r', pcap_path, '-Y', 'ssl.handshake.type == 1', '-T', 'json']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError('tshark failed: ' + (res.stderr or res.stdout))
    # We save raw tshark JSON for manual inspection; extraction logic can be added per environment.
    with open(out_json_path, 'w') as f:
        f.write(res.stdout)
    return out_json_path

def analyze_structured_clienthello(ch):
    # ch: dict with expected keys per schema
    version = ch.get('version', 771)  # TLS 1.3 default numeric 771
    ciphers = ch.get('ciphers', [])
    extensions = ch.get('extensions', [])
    curves = ch.get('groups', [])
    ecpoints = ch.get('ec_point_formats', [])
    alpn = ch.get('alpn', [])
    key_shares = ch.get('key_shares', [])

    ja3 = ja3_from_fields(version, ciphers, extensions, curves, ecpoints)
    ja3_md5 = ja3_hash(ja3)
    ja4 = ja4_from_fields(alpn, key_shares)

    return {
        'ja3_string': ja3,
        'ja3_md5': ja3_md5,
        'ja4_string': ja4,
        'alpn': alpn,
        'ciphers': ciphers,
        'extensions': extensions,
        'groups': curves,
        'ec_point_formats': ecpoints,
        'key_shares': key_shares
    }

def compare_to_metadata(report, metadata):
    diffs = {}
    # Compare ALPN sets and order (exact match required by spec)
    meta_alpn = metadata.get('alpn', [])
    diffs['alpn_match'] = (report['alpn'] == meta_alpn)
    diffs['alpn_expected'] = meta_alpn
    # Compare extension order (exact match required by spec doc)
    diffs['ext_order_match'] = (report['extensions'] == metadata.get('extensions', []))
    diffs['ext_expected'] = metadata.get('extensions', [])
    # Compare JA3 MD5 equality (exact)
    diffs['ja3_match'] = (report['ja3_md5'] == metadata.get('ja3_md5'))
    diffs['ja3_expected'] = metadata.get('ja3_md5')
    return diffs

def main():
    parser = argparse.ArgumentParser(description='ClientHello analysis CLI (safe)')
    parser.add_argument('--input', '-i', required=True, help='Path to structured ClientHello JSON or PCAP')
    parser.add_argument('--compare', '-c', help='Path to chrome metadata JSON to compare against (optional)')
    parser.add_argument('--output', '-o', help='Path to write JSON report', default='analysis_report.json')
    args = parser.parse_args()

    input_path = args.input
    structured = None
    if input_path.lower().endswith('.pcap') or input_path.lower().endswith('.pcapng'):
        # attempt to extract via tshark
        try:
            tmp_json = input_path + '.tshark.json'
            extract_clienthello_from_tshark(input_path, tmp_json)
            print('Wrote tshark JSON to', tmp_json)
            # Attempt to parse the tshark JSON into our structured schema
            try:
                structured = parse_tshark_json(tmp_json)
                print('Parsed ClientHello from tshark JSON')
            except Exception as e:
                print('Parsing tshark JSON failed:', e)
                print('Please convert tshark JSON into structured ClientHello JSON and re-run the CLI.')
                sys.exit(2)
        except Exception as e:
            print('tshark extraction failed:', e)
            sys.exit(2)
    else:
        structured = load_json(input_path)

    report = analyze_structured_clienthello(structured)
    if args.compare:
        metadata = load_json(args.compare)
        diffs = compare_to_metadata(report, metadata)
    else:
        diffs = None

    out = {'report': report, 'diffs': diffs}
    with open(args.output, 'w') as f:
        json.dump(out, f, indent=2)
    print('Wrote analysis to', args.output)

if __name__ == '__main__':
    main()
