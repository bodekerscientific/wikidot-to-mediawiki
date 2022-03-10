from page_xml import PageXMLParser

xml="<data><fullname>list-of-participants</fullname><title>List Of Participants</title><title_shown>List Of Participants</title_shown></data>"

def test_fullname():
    instance = PageXMLParser(xml)
    assert instance.fullname == "list-of-participants"

def test_title():
    instance = PageXMLParser(xml)
    assert instance.title == "List Of Participants"

