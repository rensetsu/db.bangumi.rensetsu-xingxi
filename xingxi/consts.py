from librensetsu.prettyprint import PrettyPrint, Platform, Status

pprint = PrettyPrint(Platform.BANGUMI)
RAW_DB = "bgm_raw.json"
DEST = "bangumi.json"
DESTM = "bangumi_min.json"

__all__ = ['pprint', 'Platform', 'Status']
