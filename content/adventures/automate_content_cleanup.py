fr = open("nl.yaml", "r")
fw = open("nl-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0
for line in lines:
    # Update this line for each language (manually...)
    if "## Voorbeeldcode" in line or "## Voorbeeld code" in line or "## Voorbeeld Hedy Code" in line or "## Voorbeeld Hedy code" in line:
        counter += 1
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")