"""
python run_tests.py
"""

import sys
import unittest


def run_tests() -> bool:
    suite = unittest.TestLoader().discover(
        start_dir="test", pattern="*.py", top_level_dir="."
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
