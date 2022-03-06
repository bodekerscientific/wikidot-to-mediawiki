from wikidot import WikidotToMediaWiki

def test_plain_text():
    text = "This is some plain text."
    expected = text
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    assert result == expected

def test_internal_link():
    text = "This is some text with a link to an [[[internal page]]]."
    expected = "This is some text with a link to an [[internal page]]."
    instance = WikidotToMediaWiki()
    result, links, _ = instance.convert(text)
    assert result == expected
    assert links == ["internal page"]

def test_internal_links():
    text = "This is [[[some text]]] with a link to an [[[internal page]]]."
    expected = "This is [[some text]] with a link to an [[internal page]]."
    instance = WikidotToMediaWiki()
    result, links, _ = instance.convert(text)
    assert result == expected
    assert links == ["some text", "internal page"]

def test_code():
    text = 'This is a code block: [[code type="python"]]1 + 2 == 3[[/code]]'
    expected = "This is a code block: \n <nowiki>1 + 2 == 3</nowiki>"
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    print("result:", result)
    assert result == expected

def test_linked_files():
    text = "This is a link to an image: [[image filename.png]]"
    expected = "This is a link to an image: [[File:filename.png]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_complex_images():
    text = 'This is a link to an image: [[image filename.png size="medium" alt="alternative text"]]'
    expected = "This is a link to an image: [[File:filename.png]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]
