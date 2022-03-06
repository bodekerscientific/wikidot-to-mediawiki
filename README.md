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


Uploading to New Site
---------------------

To upload the converted Wikidot pages to your MediaWiki-based site, you'll need the address of your site and a bot login.  This data needs to be saved into a file called `SECRETS.py`.

First, create the file `SECRETS.py` in this directory.  Below is an example of its contents:

    endpoint = "https://example.com/api.php"
    bot_username = "MyUsername@BotUsername"
    bot_password = "BotPassword"
    verify = True # Set to False if your site does not have a valid SSL certificate

The endpoint is the API endpoint for your MediaWiki-based site.  You can obtain the endpoint via the page `Special:ApiSandbox`.  For more detail, see the [MediaWiki API documentation](https://www.mediawiki.org/wiki/API:Main_page).

A bot login can be created at `Special:BotPasswords`.  You will need to give it the rights to:
* high-volume editing
* create, edit, and move pages
* upload new files

If your site does not have an SSL certificate, or if the certificate is self-signed, you will want to set `verify` to `False`.


Testing
-------

Run `pytest` to run all automated tests.

Run `pytest test_wikidot.py` to run the automated tests for converting Wikidot's format to MediaWiki's format.

Run `pytest test_mediawiki.py` to run the automated tests for interacting with a MediaWiki site.