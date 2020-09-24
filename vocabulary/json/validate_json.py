from jsonschema import validate
import json


def main():
    with open('mapping2.schema.json') as f_schema:
        schema = json.load(f_schema)

    with open('assay_results_numeric2.json') as f_mapping:
        instance = json.load(f_mapping)
    print(schema)
    print(instance)
    validate(instance=instance, schema=schema)


if __name__ == '__main__':
    main()
