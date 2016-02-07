#!/usr/bin/python
import os

for f in os.listdir("output"):
	stem = ".".join(f.split(".")[ : -1])
	if os.system("python convert.py -f inputnew/" + stem + ".txt -o output"):
		raise RuntimeError
