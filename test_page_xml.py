from page_xml import PageXML

def test_open_page():
    xml="<data><fullname>list-of-participants</fullname><title>List Of Participants</title><title_shown>List Of Participants</title_shown></data>"
    instance = PageXML(xml)
    assert instance.fullname == "list-of-participants"