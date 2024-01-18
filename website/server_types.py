"""Standard representations of data types used inside the server

Used mainly for passing data using HTMX
"""
from dataclasses import dataclass, field


@dataclass
class SortedAdventure:
    short_name: str
    long_name: str
    is_teacher_adventure: bool
    is_command_adventure: bool
    levels: list = field(default_factory=list)

    # Meant to be used when testing membership against
    # a list of strings
    def __hash__(self) -> int:
        return hash(self.short_name)
