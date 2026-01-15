import os
from os import path
import contextlib

prefixes_dir = path.join(path.dirname(__file__), 'prefixes')

# Define code that will be used if some turtle command is present
with open(f'{prefixes_dir}/turtle.py', encoding='utf-8') as f:
    TURTLE_PREFIX_CODE = f.read()

# Preamble that will be used for non-Turtle programs
# numerals list generated from: https://replit.com/@mevrHermans/multilangnumerals
with open(f'{prefixes_dir}/normal.py', encoding='utf-8') as f:
    NORMAL_PREFIX_CODE = f.read()

# Define code that will be used if a pressed command is used
with open(f'{prefixes_dir}/pressed.py', encoding='utf-8') as f:
    PRESSSED_PREFIX_CODE = f.read()

# Define code that will be used if music code is used
with open(f'{prefixes_dir}/music.py', encoding='utf-8') as f:
    MUSIC_PREFIX_CODE = f.read()


def is_production():
    """Whether we are serving production traffic."""
    return os.getenv('IS_PRODUCTION', '') != ''


@contextlib.contextmanager
def atomic_write_file(filename, mode='wb'):
    """Write to a filename atomically.

    First write to a unique tempfile, then rename the tempfile into
    place. Use replace instead of rename to make it atomic on windows as well.
    Use as a context manager:

        with atomic_write_file('file.txt') as f:
            f.write('hello')
    """

    tmp_file = f'{filename}.{os.getpid()}'
    with open(tmp_file, mode) as f:
        yield f

    os.replace(tmp_file, filename)