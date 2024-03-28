"""Standard representations of data types we communicate to the front end

The types defined here should agree with the types defined in `types.ts`.
(We could enforce that, but it would require additional complicated
build steps, so for now we will rely on human discipline to keep this
true).

Data classes are usually indexed as `object.field`, but much of the existing
template code expects to index as `object['field']`, so we put a magic method
on every object so that method of accessing also works.
"""

import functools
from typing import Optional, List
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
import utils


def require_kwargs(klass):
    """Decorator to require keyword arguments when instantiating a class.

    This decorator avoids having to take a dependency on Python 3.10 (which adds
    support for `@dataclass(kw_only=True)`), so people working on this project don't
    have to install a newer Python version.
    """
    ctr = klass.__init__

    @functools.wraps(ctr)
    def wrapper(self, *args, **kwargs):
        if args:
            raise RuntimeError(f'You must use only keyword arguments when instantiating {klass.__name__}')
        return ctr(self, **kwargs)
    klass.__init__ = wrapper
    return klass


@require_kwargs
@dataclass
class ExtraStory:
    text: str
    example_code: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)


@require_kwargs
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


@require_kwargs
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


def halve_adventure_content(content, max_char_length=750):
    """Splits content if its length exceeds the max_length characters (excluding tags) and sets example_code."""
    soup = BeautifulSoup(content, 'html.parser')
    text_without_tags = soup.get_text(separator='')
    text = content
    example_code = ""
    if len(text_without_tags) > max_char_length:
        # Split text at a suitable breaking point
        split_index = content.find('</p>', len(text_without_tags)//2)  # Find a closing paragraph tag.
        if split_index > -1:
            text = content[:split_index]
            example_code = content[split_index:]
        else:
            # If no suitable split point found, don't truncate content
            text = content
    return text, example_code


@require_kwargs
@dataclass
class Adventure:
    short_name: str
    name: str
    text: str
    save_name: str
    editor_contents: str = field(default='')
    is_teacher_adventure: bool = field(default=False)
    is_command_adventure: bool = field(default=False)
    image: Optional[str] = None
    example_code: Optional[str] = None
    extra_stories: Optional[List[ExtraStory]] = field(default_factory=list)
    save_info: Optional[SaveInfo] = None
    id: Optional[str] = ""
    author: Optional[str] = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    @staticmethod
    def from_teacher_adventure_database_row(row):
        text, example_code = halve_adventure_content(row.get("formatted_content", row["content"]))
        return Adventure(
            short_name=row['id'],
            name=row['name'],
            save_name=row['name'],
            editor_contents='',  # Teacher adventures don't seem to have this
            text=text,
            example_code=example_code,
            is_teacher_adventure=True,
            is_command_adventure=False)
