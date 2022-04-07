
language = """
var choice = 'en';

switch(choice){"""


printer = """
const fs = require("fs");

fs.writeFileSync("../../tests/test_highlighting/data.json", JSON.stringify(LEVELS), function(err = false) {
if(err){
  return console.log("error");
}
})
"""



file = open("../../static/js/syntaxModesRules.ts")
old_code = file.read().split("\n")
file.close()


new_code = ["#!/usr/bin/env ts-node"]
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

new_code = "\n".join(new_code)


new_file = open("../../static/js/syntaxModesRulesForTests.ts","w")
new_file.write(new_code)
new_file.close()



