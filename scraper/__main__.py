from sys import exit as sysexit
from time import time
from traceback import print_exc

from consts import Status, pprint
from librensetsu.humanclock import convert_float_to_time
from loops import do_loop


def main() -> None:
    """Main process of the util"""
    start = time()
    try:
        do_loop()
        end = time()
        pprint.print(
            Status.INFO, f"Time elapsed: {convert_float_to_time(end - start)}"
        )
        sysexit(0)
    except Exception as e:
        pprint.print(Status.ERR, f"An error occurred: {e}")
        print_exc()
        end = time()
        pprint.print(
            Status.INFO, f"Time elapsed: {convert_float_to_time(end - start)}"
        )
        sysexit(1)


if __name__ == "__main__":
    main()
