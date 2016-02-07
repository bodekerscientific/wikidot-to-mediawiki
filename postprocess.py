#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# Copyright 2016 by Christopher Mitchell
# https://github.com/KermMartian/wikidot-to-markdown
import os, re, sys

def postprocess(text):
	# NOTE: Commented out for now. If you want to do some post-processing,
	# add a body to this function. The following code shows some examples
	# of what you can do.
	return text

	# Process link corrections
	for inlink in re.finditer(r"\[\[(([^\]\|]+)(\|([^\]]+))?)\]\]", text):
		# Rename certain "categories" and rebuild the original link
		comp_link = inlink.group(2).strip()
		link_pieces = comp_link.split(":")
		if link_pieces[0] == "Z80":
			link_pieces = link_pieces[1:]

		link_pieces[0] = link_pieces[0][0].upper() + link_pieces[0][1:]
		if len(link_pieces) == 2:
			if link_pieces[0] == "Instructions-set":
				link_pieces[0] = "Opcodes"
			if link_pieces[0] in ["Directives", "Macros", "Opcodes"]:
				link_pieces[1] = link_pieces[1].upper()
			link_pieces[1] = link_pieces[1].replace("-","/")
			
		replacement = "Z80:" + ":".join(link_pieces)

		# Keep original special text, if necessary
		if None != inlink.group(4):
			replacement += "|" + inlink.group(4).strip()
		else:
			replacement += "|" + link_pieces[-1]
		#print inlink.group(1) + " -> " + replacement
		text = text.replace(inlink.group(0), "[[" + replacement + "]]")
		
	# Add categories
	text += "\n\n{{lowercase}}\n"
	text += "[[Category:Z80 Assembly]]\n"
	text += "[[Category:Z80 Heaven]]\n"

	return text
