import pandas as pd
import requests
import json

from metadata_examples import examples


def omop_domain(field):
    concept_id = int(examples[examples['field_id'] == field]['target_concept_id'].unique())
    response = requests.get(f'https://athena.ohdsi.org/api/v1/concepts/{concept_id}')
    concept = json.loads(response.text)
    domain = concept['domainId']
    return domain


def create_column_name(field_id, instance_id, array_index):
    return f'{field_id}-{instance_id}.{array_index}'


def example_omop_table(field_id, value=None, instance='0', array='0'):
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
    return table


if __name__ == '__main__':
    # Note: the arguments have to be strings, not integers.
    print(example_omop_table(field_id='47', value=None, instance='0'))
