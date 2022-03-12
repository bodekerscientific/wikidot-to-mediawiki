# Wikidot to Mediawiki converter

This repository contains two programs, a conversion program and an upload program.

The conversion program (`convert.py`) takes a backup of a Wikidot site (produced by [Wikidot-tools](https://github.com/bodekerscientific/wikidot_tools)) and produces MediaWiki-formatted text files and attachments that are ready for upload to a MediaWiki site.

The upload program (`upload.py`) takes the output of the converter and uploads the data to a MediaWiki site.

## Installation

A conda environment file is included with this repository.  To install it, you'll need to have conda installed, then run:

    conda env create --file environment.yml

Once the new environment has been created, you'll need to activate it:

    conda activate wikidot-to-mediawiki

## How to Use

There are three key steps in moving a Wikidot-based wiki to a MediaWiki-based wiki:

0. Backup the Wikidot site using [Wikidot-tools](https://github.com/bodekerscientific/wikidot_tools).
1. Convert the Wikidot-based backup to a collection of files ready for MediaWiki.
2. Upload the collection of files to MediaWiki.

### Step 0: Backup

We assume that you have already backed up your Wikidot site using [Wikidot-tools](https://github.com/bodekerscientific/wikidot_tools).

For every page in the Wikidot site, the backup produces a list of `.txt` files that are formatted in [Wikidot's Wikitext syntax](https://www.wikidot.com/doc-wiki-syntax:start).  It also produces `.html` and `.xml` files; the converter ignores these files.

For every page in the Wikidot site, the backup may also produce a directory with the same name as the page.  This directory contains files that were associated with the page.

We will, as an example, say you have saved your site's backup in `backup`.
 
### Step 1: Convert

The conversion program requires the location of the backup (_source_) and a location to store the converted files (_dest_):

    convert.py source dest

Continuing our example, if you wanted to save the converted site to the directory `conversion`, from within this directory you would run the command:

    ./convert.py backup conversion

The _dest_ directory is created if it does not already exist.

The conversion program takes the backed-up pages (the `.txt` files) and converts them to [MediaWiki-formatted pages](https://www.mediawiki.org/wiki/Help:Formatting) (saved as `.mktxt` files in the _dest_ directory).

This process works well, but does not always work perfectly.  Inconsistent syntax that was accepted by Wikidot may not be correctly processed by the converter.  It may be required to hand-edit either the original Wikidot-formatted `.txt` files, or output of the converter.

The conversion program also considers the files associated with each page.  They are renamed and saved in a single directory (_dest_/files_to_upload).  References to these new filenames are used in the converted pages.

If a file is found in the associated directory that is not referenced in the original page, then a new section will be added to the text of the converted page that lists that file.  This way upload files will not be orphaned from their associated pages.

A report (`wikidot-to-mediawiki-report.mktxt`) is produced is the _dest_ directory listing the pages that were processed by the converter.

### Step 2: Upload

To upload the converted Wikidot pages to your MediaWiki-based site, you'll need the address of your site's API endpoint and a bot login.  This data needs to be saved into a file called `SECRETS.py`.

First, create the file `SECRETS.py` in this directory.  Below is an example of its contents:

    endpoint = "https://example.com/api.php"
    bot_username = "MyUsername@BotUsername"
    bot_password = "BotPassword"
    verify = True # Set to False if your site does not have a valid SSL certificate

The endpoint is the API endpoint for your MediaWiki-based site.  You can obtain the endpoint via the page `Special:ApiSandbox` on your MediaWiki site.  For more detail, see the [MediaWiki API documentation](https://www.mediawiki.org/wiki/API:Main_page).

A bot login can be created at `Special:BotPasswords` on your MediaWiki site; once the login is created, the system will give you the details for `bot_username` and `bot_password`.  You will need to give the bot login the rights to:
* high-volume editing
* create, edit, and move pages
* upload new files
* upload, replace, and move files

If your site does not have an SSL certificate, or if the certificate is self-signed, you will want to set `verify` to `False`.

Continuing with our example, once the `SECRETS.py` file is ready, you can run the upload program with the command:

    ./upload.py conversion

The conversion of your Wikidot-based site will now be found on your MediaWiki site.  To look at the list of recently added files, see the page `Special:RecentChanges` on your MediaWiki site.

Testing
-------

Run `pytest` to run all automated tests.

Run `pytest test_wikidot.py` to run the automated tests for converting Wikidot's format to MediaWiki's format.

Run `pytest test_mediawiki.py` to run the automated tests for interacting with your MediaWiki site.  These tests may place files on your MediaWiki site.  For a list of recently added files, see the page `Special:RecentChanges` on your MediaWiki site.