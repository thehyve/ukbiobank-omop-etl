# Copyright 2020 The Hyve
#
# Licensed under the GNU General Public License, version 3,
# or (at your option) any later version (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# !/usr/bin/env python3
import csv
from pathlib import Path
from typing import Dict
import logging

from src.Python.model.usagi_object import UsagiObject, FieldMapping

logger = logging.getLogger(__name__)


class Target:

    def __init__(self):
        self.concept_id = None
        self.value_as_concept_id = None
        self.value_as_number = None
        self.unit_concept_id = None
        self.source_value = None
        self.value_source_value = None

        self.variable_comment = None
        self.value_comment = None

    def __str__(self):
        return f'{self.source_value}-{self.value_source_value} => ' \
               f'concept_id: {self.concept_id}, ' \
               f'value_as_concept_id: {self.value_as_concept_id}, ' \
               f'value_as_number: {self.value_as_number}, ' \
               f'unit_concept_id: {self.unit_concept_id}, ' \
               f'source_value: {self.source_value}, ' \
               f'value_source_value: {self.value_source_value}, ' \
               f'variable_comment: {self.variable_comment}, ' \
               f'value_comment: {self.value_comment}'


class FieldConceptMapper:
    def __init__(self, in_directory: Path, verbose: bool = False):
        self.field_mappings: Dict[int, FieldMapping] = {}
        self.verbose = verbose
        self.load(in_directory)

    def __call__(self, field_id: int, value: str) -> Target:
        return self.lookup(field_id, value)

    def load(self, directory: Path):
        if not directory.exists():
            raise FileNotFoundError(f"No such directory: '{directory}'")

        for usagi_path in directory.glob('*.csv'):
            if self.verbose:
                print(f"Loading {usagi_path.name}...")
            self._load_usagi(usagi_path)

    @staticmethod
    def _load_map(file_path: Path):
        with file_path.open(encoding='ISO-8859-2') as f_in:
            for row in csv.DictReader(f_in):
                yield row

    def _load_usagi(self, file_path: Path):
        for row in self._load_map(file_path):
            usagi_mapping = UsagiObject(row)
            field_id = usagi_mapping.field_id
            # TODO: ignore status
            codemapping = self.field_mappings.setdefault(field_id, FieldMapping(field_id))
            codemapping.add(usagi_mapping)

    def has_mapping_for_field(self, field_id: int):
        return field_id in self.field_mappings

    def lookup(self, field_id: int, value: str) -> Target:
        """
        For given variable/value pair, looks up the target concept_id, value_as_concept_id, value_as_number and unit_concept_id.
        The mapping can be one of three types:
        1. Only concept. Variable and value together map to one concept_id.
        2. Categorical. Variable maps to a concept_id, value maps to a value_as_concept_id.
        3. Numeric. If no mapping for value found, the value is assumed to be numeric. Variable maps to concept_id and unit_concept_id. Value is converted to float.
        :param field_id: integer
        :param value: string
        :return: Target
        """
        target = Target()
        target.value_source_value = value

        if not self.has_mapping_for_field(field_id):
            target.concept_id = 0
            target.source_value = field_id
            return target

        # Get concept_id from from variable and value separately
        field_mapping = self.field_mappings[field_id]
        target.concept_id = field_mapping.event_mapping.concept_id
        target.source_value = field_id

        if field_mapping.has_unit():
            target.value_as_number = float(value)
            target.unit_concept_id = field_mapping.unit_mapping.concept_id
        elif field_mapping.has_values():
            value_mapping = field_mapping.values.get(value)
            if value_mapping:
                target.value_as_concept_id = value_mapping.concept_id
            else:
                print(f'Value "{value}" for field_id {field_id} is unknown')

        return target


if __name__ == '__main__':
    mapper = FieldConceptMapper(Path('./resources/usagi_input'))

    # Some simple tests
    print(mapper.lookup(41256, '0552'))
    print(mapper.lookup(30785, '8'))
