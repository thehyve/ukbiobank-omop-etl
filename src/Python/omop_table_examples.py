import pandas as pd
import requests
import json
from IPython.display import display

from src.Python.metadata_examples import examples


def omop_domain(field):
    concept_id = int(examples[examples['field_id'] == field]['target_concept_id'].unique())
    response = requests.get(f'https://athena.ohdsi.org/api/v1/concepts/{concept_id}')
    concept = json.loads(response.text)
    domain = concept['domainId']
    return domain


def example_omop_table(field, instance, *value):
    domain = omop_domain(field)
    if value:
        row = examples[(examples['field_id'] == field) & (examples['value'] == value)]
    else:
        row = examples[examples['field_id'] == field]

    table = pd.Series({'person_id': 'get(eid)',
                       domain + '_concept_id': str(row.iloc[0]['target_concept_id']),
                       domain + '_date': 'get date from field ' + str(row.iloc[0]['date_field_id']) + '-' + instance,
                       'value_as_concept_id': str(row.iloc[0]['target_value_concept_id']),
                       'value_as_number': 'get value from field ' + str(row.iloc[0]['field_id']) + '-' + instance,
                       'unit_concept_id': str(row.iloc[0]['unit_concept_id'])
                       })
    return table


display(example_omop_table(2986, '0.1', 0))
