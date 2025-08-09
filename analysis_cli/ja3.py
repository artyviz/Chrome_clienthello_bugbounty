# Lightweight JA3 / JA4 computation helpers
# JA3: SSLVersion,CipherSuites,Extensions,EllipticCurves,ECPointFormats
# JA4: TLS version, cipher, extensions, alpn, key_share? (simplified here)
from typing import List, Dict

def canonical_list_str(vals: List[int]) -> str:
    return '-'.join(str(v) for v in vals)

def ja3_from_fields(version: int, ciphers: List[int], extensions: List[int], curves: List[int], ecpoints: List[int]) -> str:
    """Compute a JA3 string from the provided ClientHello fields."""
    parts = [
        str(version),
        canonical_list_str(ciphers),
        canonical_list_str(extensions),
        canonical_list_str(curves),
        canonical_list_str(ecpoints)
    ]
    return ','.join(parts)

def ja3_hash(ja3_str: str) -> str:
    import hashlib
    return hashlib.md5(ja3_str.encode('utf-8')).hexdigest()

def ja4_from_fields(alpn_list: List[str], key_share_groups: List[int]=None) -> str:
    # Simplified JA4: ALPN list + key_share groups (if present)
    parts = []
    parts.append('|'.join(alpn_list))
    if key_share_groups:
        parts.append('-'.join(str(x) for x in key_share_groups))
    return '|'.join(parts)
