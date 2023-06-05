"""Standard representations of data types we communicate to the front end

The types defined here should agree with the types defined in `types.ts`.
(We could enforce that, but it would require additional complicated
build steps, so for now we will rely on human discipline to keep this
true).

Data classes are usually indexed as `object.field`, but much of the existing
template code expects to index as `object['field']`, so we put a magic method
on every object so that method of accessing also works.
"""

from typing import Optional, List
from dataclasses import dataclass, field
import utils


@dataclass
class ExtraStory:
    text: str
    example_code: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass
class Program:
    id: str
    name: str
    code: str
    date: int

    # The adventure name this program was written under
    #
    # - For built-in adventures, the short_name of the adventure
    # - For teacher-written adventures:
    #    - either the `id` of the teacher adventure (new); or
    #    - the (display) `name` of the teacher adventure (old)
    adventure_name: str
    public: Optional[int] = None
    submitted: Optional[bool] = None

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_database_row(r):
        """Convert a database row into a typed Program object."""
        return Program(
            name=r.get('name', ''),
            code=r.get('code', ''),
            date=r.get('date', 0),
            adventure_name=r.get('adventure_name', 'default'),
            id=r.get('id', ''),
            public=r.get('public'),
            submitted=r.get('submitted'))


@dataclass
class SaveInfo:
    id: str
    public: Optional[int] = None
    submitted: Optional[bool] = None
    public_url: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_program(program: Program):
        return SaveInfo(
            id=program.id,
            public=program.public,
            submitted=program.submitted,
            public_url=f'{utils.base_url()}/hedy/{program.id}/view' if program.public or program.submitted else None,
        )


@dataclass
class Adventure:
    short_name: str
    name: str
    text: str
    save_name: str
    start_code: str
    is_teacher_adventure: bool
    is_command_adventure: bool
    image: Optional[str] = None
    example_code: Optional[str] = None
    extra_stories: Optional[List[ExtraStory]] = field(default_factory=list)
    save_info: Optional[SaveInfo] = None

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_teacher_adventure_database_row(row):
        return Adventure(
            short_name=row['id'],
            name=row['name'],
            save_name=row['name'],
            start_code='',  # Teacher adventures don't seem to have this
            text=row['content'],
            is_teacher_adventure=True,
            is_command_adventure=False)
