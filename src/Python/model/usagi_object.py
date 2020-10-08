# !/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Dict, Optional


class MappingStatus(Enum):
    UNCHECKED = 1
    APPROVED = 2
    IGNORED = 3
    FLAGGED = 4


class MappingType(Enum):
    EVENT = 1
    VALUE = 2
    UNIT = 3


class UsagiObject:

    def __init__(self, row):
        self.field_id: int = int(row['sourceCode'])
        self.value_code: str = row['sourceValueCode']
        self.target: TargetMapping = TargetMapping(row)
        self.type: MappingType = MappingType[row['mappingType']]
        # self.mapping_status: MappingStatus = MappingStatus[row['mappingStatus']]
        # self.status_set_by: str = row['statusSetBy']
        # self.status_set_on: datetime = datetime.fromtimestamp(int(row['statusSetOn']))
        # self.target_concept_id: int = int(row['conceptId'])
        # self.mapping_type: MappingType = MappingType[row['mappingType']]
        # self.comment: str = row['comment']
        # self.created_by: str = row['createdBy']
        # self.created_on: datetime = datetime.fromtimestamp(row['createdOn'])


class TargetMapping:

    def __init__(self, row):
        self.concept_id: int = int(row['conceptId'])
        self.created_by: str = row['createdBy']
        self.created_on: datetime = datetime.fromtimestamp(int(row['createdOn'])/1000)
        self.status: MappingStatus = MappingStatus[row['mappingStatus']]
        self.status_set_by: str = row['statusSetBy']
        self.status_set_on: datetime = datetime.fromtimestamp(int(row['statusSetOn'])/1000)
        self.comment: str = row['comment']

        # self.concept_id: int
        # self.status: MappingStatus
        # self.status_set_by: str
        # self.status_set_on: datetime
        # self.comment: str
        # self.created_by: str
        # self.created_on: str


class FieldMapping:

    def __init__(self, field_id: int):
        self.field_id: int = field_id

        # Initialize
        # TODO: for the same field, different value can map differently
        # TODO: so store for every discrete mapping also the event_mapping for each value.
        self.event_mapping: Optional[TargetMapping] = None
        self.unit_mapping: Optional[TargetMapping] = None
        self.values: Dict[str, TargetMapping] = {}

    def add(self, usagi_mapping: UsagiObject):
        if usagi_mapping.type == MappingType.EVENT:
            if self.event_mapping:
                # TODO: this will actually happen for field with multiple values.
                print(f'Warning: {self.field_id} already has a event_concept_id assigned.')
                return
            self.event_mapping = usagi_mapping.target
        elif usagi_mapping.type == MappingType.UNIT:
            if self.unit_mapping:
                print(f'Warning: {self.field_id} already has a unit_concept_id assigned.')
                return
            self.unit_mapping = usagi_mapping.target
        elif usagi_mapping.type == MappingType.VALUE:
            if usagi_mapping.value_code in self.values:
                print(f'Warning: {self.field_id}-{usagi_mapping.value_code} already has a value_concept_id assigned.')
                return
            self.values[usagi_mapping.value_code] = usagi_mapping.target
        else:
            print(f'Warning: unknown Mapping Type "{usagi_mapping.type}"')

    def has_unit(self) -> bool:
        return self.unit_mapping is not None

    def has_values(self) -> bool:
        return bool(self.values)
