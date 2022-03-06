from wikidot import WikidotToMediaWiki

def test_plain_text():
    text = "This is some plain text."
    expected = text
    instance = WikidotToMediaWiki()
    result, _ = instance.convert(text)
    assert result == expected

def test_internal_link():
    text = "This is some text with a link to an [[[internal page]]]."
    expected = "This is some text with a link to an [[internal page]]."
    instance = WikidotToMediaWiki()
    result, links = instance.convert(text)
    assert result == expected
    assert links == ["internal page"]

def test_internal_links():
    text = "This is [[[some text]]] with a link to an [[[internal page]]]."
    expected = "This is [[some text]] with a link to an [[internal page]]."
    instance = WikidotToMediaWiki()
    result, links = instance.convert(text)
    assert result == expected
    assert links == ["some text", "internal page"]

def test_code():
    text = 'This is a code block: [[code type="python"]]1 + 2 == 3[[/code]]'
    expected = "This is a code block: \n <nowiki>1 + 2 == 3</nowiki>"
    instance = WikidotToMediaWiki()
    result, _ = instance.convert(text)
    print("result:", result)
    assert result == expected

