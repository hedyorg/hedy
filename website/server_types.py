"""Standard representations of data types used inside the server

Used mainly for passing data using HTMX
"""

from dataclasses import dataclass


@dataclass
class SortedAdventure:
    short_name: str
    long_name: str
    is_teacher_adventure: bool
    is_command_adventure: bool

    # Meant to be used when testing membership against
    # a list of strings
    def __hash__(self) -> int:
        return hash(self.short_name)
