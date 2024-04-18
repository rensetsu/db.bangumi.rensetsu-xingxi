# Rensetsu Service Scraper for Bangumi.tv

This is a command-line utility to scrape Bangumi data and convert it to
Rensetsu Media object format

## Requirements

* Python >= 3.10

## Setup

Simply running following commands before using the app:

```sh
git clone https://github.com/rensetsu/db.bangumi.rensetsu-xingxi
cd db.bangumi.rensetsu-xingxi
python3 -m venv venv
source ./venv/bin/activate
pip install -U -r requirements.txt
```

## Usage

```sh
python xingxi
```

## License

This repo is licensed under [MIT License](LICENSE), unless stated otherwise.

## Attribution

The raw data were provided by [`bangumi-data`][bgm] project, which is licensed
under CC BY 4.0. The data were converted to Rensetsu Media object format by
[`rensetsu`][rensetsu] project, which is licensed under MIT License.

[bgm]: https://github.com/bangumi-data/bangumi-data
[rensetsu]: https://github.com/rensetsu
