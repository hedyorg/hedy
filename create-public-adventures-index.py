from website.database import PUBLIC_ADVENTURES_INDEXES, ADVENTURES


def create_multi_index_table(record):
    lang_value = record.get("language", "en")
    id = record.get("id")
    date = record.get("date")
    PUBLIC_ADVENTURES_INDEXES.put({"field#value": f"lang#{lang_value}", "date#adventure_id": f"{date}#{id}"})
    levels = record.get("levels")
    if not levels:
        levels = [record.get("level")]
    for level in levels:
        PUBLIC_ADVENTURES_INDEXES.put({"field#value": f"level#{level}", "date#adventure_id": f"{date}#{id}"})
    tags = record.get("tags", [])
    for tag in tags:
        PUBLIC_ADVENTURES_INDEXES.put({"field#value": f"tag#{tag}", "date#adventure_id": f"{date}#{id}"})


def get_indexes():
    indexes = PUBLIC_ADVENTURES_INDEXES.get_all({"field#value": "lang#en"})
    filter_fields = {}
    for i in indexes:
        field, value = i.get("field#value").split("#")
        if filter_fields.get(field):
            filter_fields[field].append(value)
        else:
            filter_fields[field] = [value]

        time_id = i.get("date#adventure_id")

        print(field, value)
        print(time_id)


def main():
    for record in ADVENTURES.get_all({"public": 1}):
        create_multi_index_table(record)
    # get_indexes()


if __name__ == "__main__":
    main()
