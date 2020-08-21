import click
import glob
import pandas as pd
import requests
import json


def read_data():
    path = "../../vocabulary/*.csv"
    examples = pd.DataFrame()
    for file in glob.glob(path):
        approach = pd.read_csv(file, dtype=object)
        examples = examples.append(approach, ignore_index=True, sort=False)
    return examples


def omop_info(concept_id):
    response = requests.get(f'https://athena.ohdsi.org/api/v1/concepts/{concept_id}')
    concept = json.loads(response.text)
    info = {'name': concept['name'], 'vocab': concept['vocabularyId'], 'domain': concept['domainId']}
    return info


@click.command()
@click.argument('field')
def lookup_metadata(field):
    examples = read_data()
    row = examples[examples['field_id'] == field]
    #value_names = row['value_name'].values.tolist()
    row = row.iloc[0]
    info1 = omop_info(row['target_concept_id'])
    info2 = omop_info(row['unit_concept_id'])
    print(f"Field_ id {row['field_id']} '{row['name']}' is mapped using the '{row['mapping_approach']}' approach")
    print(f"date_field_id: {row['date_field_id']}")
    print(f"target_concept_id: {row['target_concept_id']} ({info1['name']}, {info1['vocab']}, {info1['domain']})")
    print(f"unit_concept_id: {row['unit_concept_id']} ({info2['name']})")
    print(f"conversion factor: {row['conversion_factor']}")
    #print(f"The values it can take are {value_names}")


if __name__ == "__main__":
    lookup_metadata()
