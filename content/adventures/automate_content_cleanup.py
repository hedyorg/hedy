fr = open("en.yaml", "r")
fw = open("en-cleaned.yaml", "w")

lines = fr.readlines()
counter = 0
empty_counter = 0
for line in lines:
    # Update this line for each language (manually...)
    if "## Example code" in line or "## Example Hedy code" in line or "## Example Hedy Code" in line:
        counter += 1
    elif not line.strip():
        empty_counter += 1
    else:
        fw.write(line)
print(f"We have deleted {counter} lines")
print(f"We have deleted {empty_counter} empty lines")