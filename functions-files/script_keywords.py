import os

# Define the string to be added at the beginning of each file
definitions = "define: define\ndef: def\ncall: call\nusing: using\nwith: with\nreturn: return\n"

# Set the path to the directory containing the YAML files
path = 'content/keywords'

# Loop through each file in the directory
for filename in os.listdir(path):
    if filename.endswith('.yaml'):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r+') as file:
            content = file.read()
            file.seek(0, 0)
            file.write(definitions + content)
            file.truncate()
            file.close()