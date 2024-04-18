from dataclasses import dataclass


@dataclass
class SiteMeta:
    title: str
    """Title of the site"""
    urlTemplate: str
    """URL template of the site"""
    type: str
    """Type of the site"""
    region: list[str] | None = None
    """Supported regions of the site"""


@dataclass
class ServiceMapping:
    site: str
    """Name of the site"""
    id: str | None = None
    """Id of the media on the site"""
    begin: str | None = None
    """Start date of the show, uses yyyy-MM-dd'T'hh:mm:ss.fff'Z'"""
    broadcast: str | None = None
    """Broadcast, uses 'R'/yyyy-MM-dd'T'hh:mm:ss.fff'Z'/RRRR"""


@dataclass
class MediaItem:
    """Information regarding the media"""

    title: str
    """Title in Native/Japanese"""
    titleTranslate: dict[str, list[str]]
    """Title in other languages"""
    type: str
    """Media Type"""
    lang: str
    """Language used in the media"""
    begin: str
    """Start date of the show, uses yyyy-MM-dd'T'hh:mm:ss.fff'Z'"""
    end: str
    """End date of the show, uses yyyy-MM-dd'T'hh:mm:ss.fff'Z'"""
    sites: list[ServiceMapping]
    """List of indexed mapping"""
    broadcast: str | None = None
    """Broadcast, uses 'R'/yyyy-MM-dd'T'hh:mm:ss.fff'Z'/RRRR"""
    comment: str | None = None
    """Comment to the show"""
    bangumi_id: int | None = None
    """Bangumi ID of the media"""
    officialWebsite: str | None = None
    """Official website of the media"""

    # get bangumi ID when loaded
    def __post_init__(self):
        bid = next((i.id for i in self.sites if i.site == "bangumi"), None)
        if bid:
            self.bangumi_id = int(bid)


@dataclass
class BangumiData:
    siteMeta: dict[str, SiteMeta]
    """Metadata of the site"""
    items: list[MediaItem]
    """Media item"""
