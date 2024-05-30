import sys
# setting path
sys.path.append('../hedy')
from website.database import PUBLIC_ADVENTURES_INDEXES, ADVENTURES


def create_multi_index_table(record):
    lang_value = record.get("language", "en")
    id = record.get("id")
    date = record.get("date")
    PUBLIC_ADVENTURES_INDEXES.put({"field_value": f"lang_{lang_value}", "date_adventure_id": f"{date}_{id}"})
    levels = record.get("levels")
    if not levels:
        levels = [record.get("level")]
    for level in levels:
        PUBLIC_ADVENTURES_INDEXES.put({"field_value": f"level_lang_{level}_{lang_value}",
                                       "date_adventure_id": f"{date}_{id}"})
        PUBLIC_ADVENTURES_INDEXES.put({"field_value": f"level_{level}", "date_adventure_id": f"{date}_{id}"})
    tags = record.get("tags", [])
    for tag in tags:
        PUBLIC_ADVENTURES_INDEXES.put({"field_value": f"tag_{tag}", "date_adventure_id": f"{date}_{id}"})


def get_indexes():
    indexes = PUBLIC_ADVENTURES_INDEXES.get_all({"field_value": "lang_en"})
    filter_fields = {}
    for i in indexes:
        field, value = i.get("field_value").split("_")
        if filter_fields.get(field):
            filter_fields[field].append(value)
        else:
            filter_fields[field] = [value]

        time_id = i.get("date_adventure_id")

        print(field, value)
        print(time_id)


def main():
    for record in ADVENTURES.get_all({"public": 1}):
        create_multi_index_table(record)
    # get_indexes()


if __name__ == "__main__":
    main()
