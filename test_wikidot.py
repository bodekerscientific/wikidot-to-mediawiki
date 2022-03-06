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

def test_gallery():
    text = "This is a gallery of images:\n[[gallery]]\n: image1.png\n: image2.jpg\n[[/gallery]]"
    expected = "This is a gallery of images:\n<gallery>\nimage1.png\nimage2.jpg\n</gallery>"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["image1.png", "image2.jpg"]

def test_complex_gallery():
    text = (
        'This is a gallery of images:\n'
        + '[[gallery size="small"]]\n'
        + ': image1.png alt="Alternative text"\n'
        + ': image2.jpg width="200px"\n'
        + '[[/gallery]]'
    )
    expected = "This is a gallery of images:\n<gallery>\nimage1.png\nimage2.jpg\n</gallery>"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["image1.png", "image2.jpg"]

def test_file():
    text = "This is a file: [[file filename]]"
    expected = "This is a file: [[Media:filename]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert result == expected
    assert linked_files == ["filename"]

def test_file_with_alt_text():
    text = "This is a [[file filename|link to a file]]."
    expected = "This is a [[Media:filename|link to a file]]."
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert result == expected
    assert linked_files == ["filename"]

def test_file_example():
    text = "[[file proposal.pdf|Here]] is the proposal that was submitted."
    expected = "[[Media:proposal.pdf|Here]] is the proposal that was submitted."
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert result == expected
    assert linked_files == ["proposal.pdf"]
    
def test_file_example2():
    text = "|| [[file filename]] ||"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert linked_files == ["filename"]

def test_file_example3():
    text = "* [[file filename with spaces-hypens_underscores.pdf| Description with spaces.]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert linked_files == ["filename with spaces-hypens_underscores.pdf"]

def test_file_example4():
    text = "[[file filename ]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert linked_files == ["filename"]

def test_file_example5():
    text = "[[file filename | alternative text]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    assert linked_files == ["filename"]

def test_file_excessive_matching():
    text = (
        "If I have the contents, say 'file filename' outside of a tag, it should not be replaced"
        + " when I have a file tag with the same contents [[file filename]]."
    )
    expected = (
        "If I have the contents, say 'file filename' outside of a tag, it should not be replaced"
        + " when I have a file tag with the same contents [[Media:filename]]."
    )
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename"]
