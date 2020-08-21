import click
import glob
import pandas as pd


def read_data():
    path = "../../vocabulary/*.csv"
    examples = pd.DataFrame()

    for file in glob.glob(path):
        approach = pd.read_csv(file, dtype=object)
        examples = examples.append(approach, ignore_index=True, sort=False)
    return examples


@click.command()
@click.argument('field')
def lookup_metadata(field):
    examples = read_data()
    row = examples[examples['field_id'] == field]
    #value_names = row['value_name'].values.tolist()
    row = row.iloc[0]
    print(f"The field_ id {row['field_id']}; {row['name']} is mapped to the target concept id {row['target_concept_id']}")
    print(f"The mapping approach to take is {row['mapping_approach']}")
    print(f"The date when the data was recorded is given in {row['date_field_id']}")
    print(f"The unit concept id is {row['unit_concept_id']} and the conversion factor is {row['conversion_factor']}")
    #print(f"The values it can take are {value_names}")


if __name__ == "__main__":
    lookup_metadata()
