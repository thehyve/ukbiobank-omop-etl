# !/usr/bin/env python3
from typing import Dict, Optional
from src.Python.model.UsagiRow import UsagiRow, TargetMapping, MappingType


class ValueMapping:

    def __init__(self, value_code: str):
        self.value_code: str = value_code

        # Initialize
        self.event_mapping: Optional[TargetMapping] = None
        self.value_mapping: Optional[TargetMapping] = None


class FieldMapping:

    def __init__(self, field_id: str):
        self.field_id: str = field_id

        # Initialize
        self.event_mapping: Optional[TargetMapping] = None
        self.unit_mapping: Optional[TargetMapping] = None
        self.values: Dict[str, ValueMapping] = {}
        self.comment: Optional[str] = None

    def has_unit(self) -> bool:
        # TODO: what about numeric mappings that do not have an unit assigned?
        return self.unit_mapping is not None

    def has_values(self) -> bool:
        # TODO: what about numeric mappings that also have a few codes (-1, -3)
        return bool(self.values)

    def add(self, usagi_row: UsagiRow):
        """
        If value_code is given, unit mapping is ignored with warning.
        If no value_code is given, value mapping is ignored with warning.
        :param usagi_row:
        :return:
        """
        self.comment = usagi_row.comment
        if usagi_row.field_id != self.field_id:
            # TODO: log as warnings and/or raise custom warning. Collect warnings for validation
            print(f'Warning: given field_id "{usagi_row.field_id}" does not match field_id of mapping object "{self.field_id}". Row is skipped.')
            return

        is_value_mapping = bool(usagi_row.value_code)
        if is_value_mapping:
            self._add_value_mapping(usagi_row)
        else:
            self._add_regular_mapping(usagi_row)

    def _add_regular_mapping(self, usagi_row: UsagiRow):
        if usagi_row.type == MappingType.EVENT:
            if self.event_mapping:
                print(f'Warning: {self.field_id} already has a event_concept_id assigned and will be overwritten.')
                return
            self.event_mapping = usagi_row.target
        elif usagi_row.type == MappingType.UNIT:
            if self.unit_mapping:
                print(f'Warning: {self.field_id} already has a unit_concept_id assigned and will be overwritten.')
                return
            self.unit_mapping = usagi_row.target
        elif usagi_row.type == MappingType.VALUE:
            if usagi_row.value_code:
                print(f'Warning: please use the method "self._add_value_mapping" for adding value mappings {usagi_row}')
            else:
                print(f'Warning: no value code given in the usagi input row for field usagi_row {usagi_row}')
            print(f'Warning: mapping is not added {usagi_row}')
            return
        else:
            print(f'Warning: unknown MappingType "{usagi_row.type}"')

    def _add_value_mapping(self, usagi_row: UsagiRow):
        value_mapping = self.values.setdefault(usagi_row.value_code, ValueMapping(usagi_row.value_code))

        if self.event_mapping:
            print(f'Warning: {self.field_id} already has an event_concept_id assigned and we are trying to add a value. ?')
        if self.unit_mapping:
            print(f'Warning: {self.field_id} already has an unit_concept_id assigned and we are trying to add a value. ?')

        if usagi_row.type == MappingType.EVENT:
            if value_mapping.event_mapping:
                print(f'Warning: {self.field_id}-{value_mapping.value_code} already has a event_concept_id assigned and will be overwritten.')
                return
            value_mapping.event_mapping = usagi_row.target
        elif usagi_row.type == MappingType.UNIT:
            print(f'Warning: if value given as code, we expect no unit {usagi_row}.')
            return
        elif usagi_row.type == MappingType.VALUE:
            if value_mapping.value_mapping:
                print(f'Warning: {self.field_id}-{value_mapping.value_code} already has a value_concept_id assigned.')
                return
            value_mapping.value_mapping = usagi_row.target
        else:
            print(f'Warning: unknown MappingType "{usagi_row.type}"')
