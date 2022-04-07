
import json
 
file = open('data.json') 
data = json.load(file)
file.close()

file = open('tests.json') 
tests = json.load(file)
file.close()

print(tests)