import unittest
from tools.validate import validate


class BankIntegrityTest(unittest.TestCase):
    def test_integrity(self):
        errors, count = validate()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 10)


if __name__ == '__main__':
    unittest.main()
