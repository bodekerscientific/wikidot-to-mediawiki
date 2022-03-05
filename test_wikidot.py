from wikidot import WikidotToMarkdown

def test_plain_text():
    text = "This is some plain text."
    expected = text
    instance = WikidotToMarkdown()
    result = instance.convert(text)
    assert result == expected

def test_internal_link():
    text = "This is some text with a link to an [[[internal page]]]."
    expected = "This is some text with a link to an [[internal page]]."
    instance = WikidotToMarkdown()
    result = instance.convert(text)
    assert result == expected


