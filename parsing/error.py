from dataclasses import dataclass
from enum import Enum

from parsing import HedyMarker


class HedyParseErrorType(str, Enum):
    FATAL = "FATAL"
    RECOVERABLE = "RECOVERABLE"


class HedyParseErrorCategory(str, Enum):
    QUOTATIONS = "QUOTATIONS"
    INDENTATION = "INDENTATION"
    WHITESPACE = "WHITESPACE"
    UNKNOWN_COMMAND = "UNKNOWN_COMMAND"
    BAD_COMMAND = "BAD_COMMAND"


@dataclass
class HedyParseError:
    marker: HedyMarker
    type: HedyParseErrorType
    category: HedyParseErrorCategory
    message: str
