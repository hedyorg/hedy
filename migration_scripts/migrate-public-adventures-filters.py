# setting path
from website.database import PUBLIC_ADVENTURE_FILTERS, ADVENTURES
import sys
sys.path.append('../hedy')


def create_filters_table(record):
    lang_value = record.get("language", "en")
    levels = record.get("levels")
    if not levels:
        levels = [record.get("level")]
    for level in levels:
        value = f"{lang_value}_{level}"
        PUBLIC_ADVENTURE_FILTERS.put({"field": "lang_level", "value": value})
    tags = record.get("tags", [])
    for tag in tags:
        PUBLIC_ADVENTURE_FILTERS.put({"field": "tag", "value": tag})


def main():
    for record in ADVENTURES.get_all({"public": 1}):
        create_filters_table(record)


if __name__ == "__main__":
    main()
