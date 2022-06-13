fr = open("fr.yaml", "r")
fw = open("fr-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0

to_clean = ["## Exemple de code", "## Example code", "## Example Hedy Code", "## Example Hedy code"]

for line in lines:
    for option in to_clean:
        if option in line:
            # This is needed due to how Weblate stores the YAML files: all on one line, remove only the relevant part
            if "example_code:" in line or "example_code_2:" in line or "example_code_3:" in line or "story_text" in line:
                start_index = line.index(option)
                end_index = start_index + line[start_index:].index("\\n")
                fixed_line = line[:start_index] + line[end_index+2:]
                while fixed_line[:2] == "\\n":
                    fixed_line = fixed_line[2:]
                fw.write(fixed_line)
            counter += 1
            break
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")