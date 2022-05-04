with open("zh_Hans.yaml", "r") as r:
    lines = r.readlines()

with open("zh_Hans_without_images.yaml", "w") as w:
    counter = 0
    for line in lines:
        if "image: " not in line:
            w.write(line)
        else:
            counter += 1
    print(f"{counter} lines deleted")
