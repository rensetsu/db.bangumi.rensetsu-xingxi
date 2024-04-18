from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from json import dump, loads
from typing import Any
from uuid import uuid4

from alive_progress import alive_bar as abr
from bgmmodels import BangumiData, MediaItem
from consts import DEST, DESTM, RAW_DB, Status, pprint
from librensetsu.formatter import remove_empty_keys
from librensetsu.humanclock import translate_season
from librensetsu.models import Date, MediaInfo, RelationMaps
from dacite import from_dict


def process_item(item: MediaItem, data_uuid: str | None = None) -> MediaInfo:
    """
    Process the item on the list to convert as a MediaInfo
    :param item: Bangumi MediaItem
    :type item: MediaItem
    :param data_uuid: UUID of the data
    :type data_uuid: str
    :return: MediaInfo
    :rtype: MediaInfo
    """
    eng = None
    synonyms = None
    if item.titleTranslate:
        eng = item.titleTranslate.get("en", [])
        if eng:
            eng = eng[0]
        # recursively get all the synonyms from a dict of list of strings
        synonyms = [
            j
            for i in item.titleTranslate.values()
            for j in i
            if j != eng or j != item.title
        ]
    media_type = "ONA" if item.type == "web" else item.type
    start = datetime.fromisoformat(item.begin) if item.begin else None
    fstart = Date.from_datetime(start) if start else None
    season = None
    if fstart:
        season = translate_season(fstart)
    lang = item.lang
    match lang:
        case "ja":
            country = "JP"
        case "zh-Hans":
            country = "CN"
        case "en":
            country = "US"
        case _:
            country = None
    end = datetime.fromisoformat(item.end) if item.end else None
    return MediaInfo(
        uuid=data_uuid or str(uuid4()),
        title_display=item.title,
        title_english=str(eng) if eng else None,
        title_native=item.title,
        title_transliteration=None,
        synonyms=synonyms,
        is_adult=None,
        media_type="anime",
        media_sub_type=media_type,
        year=start.year if start else None,
        start_date=Date.from_datetime(start) if start else None,
        end_date=Date.from_datetime(end) if end else None,
        season=season,
        unit_order=None,
        unit_counts=None,
        subunit_order=None,
        subunit_counts=None,
        volume_order=None,
        volume_counts=None,
        picture_urls=[],
        country_of_origin=country,
        mappings=RelationMaps(
            bangumi=item.bangumi_id,
        ),
        source_data="bangumi",
    )


def do_loop() -> list[MediaInfo]:
    """
    Loops all the object to convert as a list of MediaInfo
    :return: List of `MediaInfo`
    :rtype: MediaInfo
    """
    try:
        with open(DEST, "r") as f:
            old_data: list[dict[str, Any]] = loads(f.read())
    except FileNotFoundError:
        old_data = []
    loi = len(old_data)
    new_data: list[MediaInfo] = []
    pprint.print(Status.INFO, "Processing data...")
    with open(RAW_DB, "r") as f:
        data = loads(f.read())
    bgm = from_dict(BangumiData, data)
    with abr(total=len(bgm.items)) as bar:  # type: ignore
        for entry in bgm.items:
            bar()
            media_id = entry.bangumi_id
            data_uuid = None
            if loi > 0:
                for odata in old_data:
                    if odata["mappings"]["bangumi"] == media_id:
                        data_uuid = odata["uuid"]
                        break
            final = process_item(entry, data_uuid)
            new_data.append(final)
    pprint.print(Status.PASS, "Data processed.")
    pprint.print(Status.INFO, "Completed loop, converting dataclasses to dict")
    new_data = [asdict(info) for info in new_data]  # type: ignore
    # sort by bangumi id
    pprint.print(Status.INFO, "Sorting by bangumi ID")
    # remove entry if the bangumi id is None
    new_data = [i for i in new_data if i["mappings"]["bangumi"] is not None]  # type: ignore
    new_data.sort(key=lambda x: x["mappings"]["bangumi"])  # type: ignore
    pprint.print(Status.INFO, "Dumping to bangumi.json")
    with open(DEST, "w") as f:
        dump(new_data, f, ensure_ascii=False)
    # remove all keys that the value is either None, empty list, or empty dict, recursively
    pprint.print(Status.INFO, "Creating bangumi_min.json")
    mininfo = deepcopy(new_data)
    mininfo = remove_empty_keys(mininfo)
    with open(DESTM, "w") as f:
        dump(mininfo, f, ensure_ascii=False)
    return new_data
