from sys import exit as sysexit
from time import time
from traceback import print_exc
from os.path import exists

from consts import Status, pprint, RAW_DB
from download import download_data
from librensetsu.humanclock import convert_float_to_time
from loops import do_loop


def main() -> None:
    """Main process of the util"""
    start = time()
    ex = 0
    pprint.print(Status.INFO, "Starting...")
    try:
        if not download_data():
            pprint.print(Status.ERR, "Failed to download Bangumi raw data, using existing data.")
        if not exists(RAW_DB):
            raise FileNotFoundError("Bangumi raw data not found")
        do_loop()
        pprint.print(Status.SUCCESS, "Finished.")
    except Exception as e:
        pprint.print(Status.ERR, f"An error occurred: {e}")
        print_exc()
        ex = 1
    end = time()
    pprint.print(
        Status.INFO, f"Time elapsed: {convert_float_to_time(end - start)}"
    )
    sysexit(ex)


if __name__ == "__main__":
    main()
