# !/usr/bin/env python3
from enum import Enum
from datetime import datetime
from src.Python.util.data_type import to_int
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


class UsagiRow:

    def __init__(self, row):
        self.field_id: str = row['sourceCode'].strip()
        self.value_code: str = row['sourceValueCode'].strip()
        self.target: TargetMapping = TargetMapping(row)
        self.type: MappingType = MappingType[row['mappingType']]
        self.comment: str = row['comment']


class TargetMapping:

    def __init__(self, row):
        self.concept_id: int = int(row['conceptId'])
        self.created_by: str = row['createdBy']
        self.created_on: datetime = datetime.fromtimestamp(to_int(row['createdOn'])/1000)
        self.status: MappingStatus = MappingStatus[row['mappingStatus']]
        self.status_set_by: str = row['statusSetBy']
        self.status_set_on: datetime = datetime.fromtimestamp(to_int(row['statusSetOn'])/1000)
