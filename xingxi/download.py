from consts import RAW_DB, Status, pprint
from fake_useragent import FakeUserAgent as FUA
from librensetsu.downloader import Downloader


def download_data() -> bool:
    """
    Download Bangumi data from bangumi-data/bangumi-data
    """
    url = "https://raw.githubusercontent.com/bangumi-data/bangumi-data/master/dist/data.json"
    headers: dict[str, str] = {
        "Accept": "application/json",
    }
    try:
        down = Downloader(
            pprint,
            url,
            RAW_DB,
            str(FUA().random),  # type: ignore
            headers,
        )
        if down.download():
            return True
        return False
    except Exception as e:
        pprint.print(Status.ERROR, f"Failed to download Bangumi data: {e}")
        return False


__all__ = ["Downloader", "pprint"]
