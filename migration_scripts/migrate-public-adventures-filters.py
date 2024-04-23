import sys
# setting path
sys.path.append('../hedy')

from website.database import PUBLIC_ADVENTURES_FILTERS, ADVENTURES

def create_filters_table(record):
    lang_value = record.get("language", "en")
    levels = record.get("levels")
    if not levels:
        levels = [record.get("level")]
    for level in levels:
        value = f"{lang_value}#{level}"
        PUBLIC_ADVENTURES_FILTERS.put({"field": "lang#level", "value": value})
    tags = record.get("tags", [])
    for tag in tags:
        PUBLIC_ADVENTURES_FILTERS.put({"field": "tag", "value": tag})


def get_filters():
    filters = PUBLIC_ADVENTURES_FILTERS.get_all({"field": "lang#level"})
    for f in filters:
        print(f)


def main():
    for record in ADVENTURES.get_all({"public": 1}):
        create_filters_table(record)
    get_filters()


if __name__ == "__main__":
    main()
