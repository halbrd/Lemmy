from LemmyGlobals import JsonPath
import json
import os

def TitleBox(string):
	return "\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n= " + string + " =\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n"

def ConfigGet(path):
	with open(os.path.join(*path)) as f:
		return json.loads(f.read())
