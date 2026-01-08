prefixes_dir = path.join(path.dirname(__file__), 'data', 'prefixes')

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


