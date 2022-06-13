fr = open("nl.yaml", "r")
fw = open("nl-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0

to_clean = ["## Voorbeeldcode", "## Voorbeeld code", "## Voorbeeld Hedy Code", "## Voorbeeld Hedy code"]

for line in lines:
    for option in to_clean:
        if option in line:
            # This is needed due to how Weblate stores the YAML files: all on one line, remove only the relevant part
            if "example_code:" in line:
                fixed_line = line.replace(option + "\\n", "")
                fw.write(fixed_line)
            counter += 1
            break
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")