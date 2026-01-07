from enum import Enum


class DocumentStatus(str, Enum):
    UNSTART = "UNSTART"
    RUNNING = "RUNNING"
    CANCEL = "CANCEL"
    DONE = "DONE"
    FAIL = "FAIL"


class NumericDocumentStatus(str, Enum):
    UNSTARTED = "0"
    RUNNING = "1"
    CANCEL = "2"
    DONE = "3"
    FAIL = "4"
