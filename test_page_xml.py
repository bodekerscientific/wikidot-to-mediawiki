from page_xml import PageXML

xml="<data><fullname>list-of-participants</fullname><title>List Of Participants</title><title_shown>List Of Participants</title_shown></data>"

def test_fullname():
    instance = PageXML(xml)
    assert instance.fullname == "list-of-participants"

def test_title():
    instance = PageXML(xml)
    assert instance.title == "List Of Participants"

