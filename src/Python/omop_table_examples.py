import pandas as pd
import requests
import json
import click
import glob


def read_data():
    path = "../../vocabulary/*.csv"
    examples = pd.DataFrame()

    for file in glob.glob(path):
        approach = pd.read_csv(file, dtype=object)
        examples = examples.append(approach, ignore_index=True, sort=False)
    return examples


def omop_domain(field):
    examples = read_data()
    concept_id = int(examples[examples['field_id'] == field]['target_concept_id'].unique())
    response = requests.get(f'https://athena.ohdsi.org/api/v1/concepts/{concept_id}')
    concept = json.loads(response.text)
    domain = concept['domainId']
    return domain


def create_column_name(field_id, instance_id, array_index):
    return f'{field_id}-{instance_id}.{array_index}'


@click.command()
@click.argument('field_id')
@click.option('--value', default=None)
@click.option('--instance', default='0')
@click.option('--array', default='0')
def example_omop_table(field_id, value, instance, array):
    examples = read_data()
    domain = omop_domain(field_id).lower()
    if value is not None:
        row = examples[(examples['field_id'] == field_id) & (examples['value'] == value)]
    else:
        row = examples[examples['field_id'] == field_id]
    row = row.iloc[0]
    table = pd.Series({'person_id': 'get(eid)',
                       domain + '_date': 'get(%s)' % create_column_name(row['date_field_id'], instance, array),
                       domain + '_concept_id': row['target_concept_id'],
                       domain + '_source_value': field_id,
                       'value_as_concept_id': row["target_value_concept_id"],
                       'value_as_number': 'get(%s)' % create_column_name(field_id, instance, array),
                       'value_source_value': value,
                       'unit_concept_id': row['unit_concept_id'],
                       domain + '_type_concept_id': 'TBD'
                       })
    table = table.dropna()
    print(domain.upper() + ' table')
    print(table)


if __name__ == '__main__':
    # Note: the arguments have to be strings, not integers.
    example_omop_table()