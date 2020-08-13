import glob
import pandas as pd
from IPython.display import display

pd.set_option('display.max_columns', 23)

path = "../../vocabulary/*.csv"
examples = pd.DataFrame()

for file in glob.glob(path):
    approach = pd.read_csv(file)
    examples = examples.append(approach, ignore_index=True)


def lookup_metadata(field):
    line = examples[examples['field_id'] == field]
    line = line.dropna(how='all', axis=1)
    return line


display(lookup_metadata(2986))
