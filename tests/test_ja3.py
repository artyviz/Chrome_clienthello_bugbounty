import unittest
from analysis_cli.ja3 import ja3_from_fields, ja3_hash

class TestJA3(unittest.TestCase):
    def test_ja3_basic(self):
        version = 771
        ciphers = [4865,4866]
        extensions = [0,11,10]
        groups = [29,23]
        ec = [0]
        s = ja3_from_fields(version, ciphers, extensions, groups, ec)
        self.assertIn('771', s)
        h = ja3_hash(s)
        self.assertEqual(len(h), 32)

if __name__ == '__main__':
    unittest.main()
