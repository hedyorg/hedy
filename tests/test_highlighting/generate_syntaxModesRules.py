
# this script modifies with tags the syntaxModesRules file
# in order to run it easily, without Ace

# We force the language
language = """
var choice = 'en';

switch(choice){"""

# We add some lines to generate a Json
printer = """
const fs = require("fs");

fs.writeFileSync("data.json", JSON.stringify(LEVELS), function(err = false) {
if(err){
  return console.log("error");
}
})
"""


# We get the code and split it line by line
file = open("../../static/js/syntaxModesRules.ts")
old_code = file.read().split("\n")
file.close()

# We create a new code with only what we are interested in
new_code = []

# for execution in a shell
new_code.append("#!/usr/bin/env ts-node")


# for each line, if we are between the tags, we will not keep the code.
# And if we are on one of the 2 special tags, we add the code pieces
flag = True
for line in old_code:
	if "#/#/@/#/#" in line:
		flag = not flag
	elif "#/#/1/#/#" in line:
		new_code.append(language)
	elif "#/#/2/#/#" in line:
		new_code.append(printer)
	elif flag :
		new_code.append(line)
	else:
		pass


# We gather all the lines of code
new_code = "\n".join(new_code)

# and save the result in a new file
new_file = open("syntaxModesRulesForTests.ts","w")
new_file.write(new_code)
new_file.close()



