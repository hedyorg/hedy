# setting path
from website.database import PUBLIC_ADVENTURE_INDEXES, ADVENTURES
import sys
sys.path.append('../hedy')


def create_multi_index_table(record):
    lang_value = record.get("language", "en")
    id = record.get("id")
    date = record.get("date")
    PUBLIC_ADVENTURE_INDEXES.put({"field_value": f"lang_{lang_value}", "date_adventure_id": f"{date}_{id}"})
    levels = record.get("levels")
    if not levels:
        levels = [record.get("level")]
    for level in levels:
        PUBLIC_ADVENTURE_INDEXES.put({"field_value": f"level_lang_{level}_{lang_value}",
                                      "date_adventure_id": f"{date}_{id}"})
        PUBLIC_ADVENTURE_INDEXES.put({"field_value": f"level_{level}", "date_adventure_id": f"{date}_{id}"})
    tags = record.get("tags", [])
    for tag in tags:
        PUBLIC_ADVENTURE_INDEXES.put({"field_value": f"tag_{tag}", "date_adventure_id": f"{date}_{id}"})


def main():
    for record in ADVENTURES.get_all({"public": 1}):
        create_multi_index_table(record)


if __name__ == "__main__":
    main()
