fr = open("nl.yaml", "r")
fw = open("nl-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0

to_clean = ["## Voorbeeldcode", "## Voorbeeld code", "## Voorbeeld Hedy Code", "## Voorbeeld Hedy code"]

for line in lines:
    for option in to_clean:
        if option in line:
            if "example_code:" in line:
                fixed_line = line.replace(option, "")
                fw.write(fixed_line)
            counter += 1
            break
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")