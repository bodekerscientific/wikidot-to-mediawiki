#!/usr/bin/python

import os

for f in os.listdir("output"):
	os.system("vim output/" + f)
	newname = raw_input("Enter article name for '" + f + "':").strip()
	os.system("php ../maintenance/edit.php -s \"Initial automated import\" \"" + newname + "\" <output/" + f)
	os.system("mv output/" + f + " complete/" + f)
