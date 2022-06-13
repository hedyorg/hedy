fr = open("en.yaml", "r")
fw = open("en-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0
for line in lines:
    # Update this line for each language (manually...)
    if "## Example code" in line or "## Example Hedy code" in line or "## Example Hedy Code" in line:
        counter += 1
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")