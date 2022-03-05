from mediawiki import MediaWiki
import SECRETS

def test_create_page():
    title = "Testing the API-based creation of a page"
    text = "This page was created by wikidot-to-mediawiki.  You may delete this page."
    instance = MediaWiki(SECRETS.endpoint, verify=SECRETS.verify)
    _ = instance.login(SECRETS.bot_username, SECRETS.bot_password)
    instance.create_page(title, text)

    # Should check here that the page was created

def test_upload_file():
    filename = "test_mediawiki__test_upload_file.txt"
    with open(filename, "wt") as f:
        f.write(
            "This file was created by wikidot-to-mediawiki to test uploading.\n"
            + "You may delete this file.\n"
        )
    
    instance = MediaWiki(SECRETS.endpoint, verify=SECRETS.verify)
    _ = instance.login(SECRETS.bot_username, SECRETS.bot_password)
    instance.upload_file("test_upload_file.txt", filename)

    # Check that the file was uploaded
    assert False