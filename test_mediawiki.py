from mediawiki import MediaWiki
import SECRETS

def test_create_page():
    title = "Testing the API-based creation of a page"
    text = "This page was created by wikidot-to-mediawiki"
    instance = MediaWiki(SECRETS.endpoint, verify=SECRETS.verify)
    result = instance.login(SECRETS.bot_username, SECRETS.bot_password)
    print("result: ",result)
    instance.create_page()

    assert False