from xml.dom.minidom import parseString

def get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

class PageXML:
    def __init__(self, xml):
        self._dom = parseString(xml)

    @property
    def fullname(self):
        data_elements = self._dom.getElementsByTagName("data")
        assert len(data_elements) == 1
        fullnames = data_elements[0].getElementsByTagName("fullname")
        assert len(fullnames) == 1
        fullname_node = fullnames[0]
        return get_text(fullname_node.childNodes)

    @property
    def title(self):
        data_elements = self._dom.getElementsByTagName("data")
        assert len(data_elements) == 1
        fullnames = data_elements[0].getElementsByTagName("title")
        assert len(fullnames) == 1
        fullname_node = fullnames[0]
        return get_text(fullname_node.childNodes)

