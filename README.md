Wikidot to Mediawiki convertor
==============================

A simple script for migrating from Wikidot to Mediawiki. Doesn't support everything but should make
your life a little easier ;)

How to Use
----------
`convert.py -f INPUT_FILE -o OUTPUT_FOLDER`

This will create a file called with the same name as the input file in the output folder.

INPUT_FILE should be formatted using [Wikidot's Wikitext format](https://www.wikidot.com/doc-wiki-syntax:start).


Getting Your Data
-----------------

Your Wikitext-formatted files can be downloaded from Wikidot using [Wikidot-tools](https://github.com/bodekerscientific/wikidot_tools).


Testing
-------

Run `pytest` to run all automated tests.