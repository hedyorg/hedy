from glob import glob
import json


def main():
    schemas = glob('content/*/*.schema.json')
    schemas = [s for s in schemas if 'generated' not in s]
    for schema_filename in schemas:
        with open(schema_filename, 'r', encoding='utf-8') as file:
            schema = json.load(file)

        schema_with_optional_fields = remove_required_fields(schema)

        output_filename = schema_filename.replace('.schema.json', '.generated.schema.json')
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            json.dump(schema_with_optional_fields, output_file)


def remove_required_fields(schema):
    if not isinstance(schema, dict):
        return schema
    else:
        return {key: remove_required_fields(value) for key, value in schema.items() if key != 'required'}


if __name__ == "__main__":
    main()
