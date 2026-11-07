"""
python -m main
"""
import logging
from pprint import pprint as pp
import cache


def main():
    
    search_text = "900 Washington Ave. Golden, CO 80401"
    pp(cache.get_and_maybe_update(search_text))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
