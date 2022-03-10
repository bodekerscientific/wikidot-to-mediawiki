from wikidot import WikidotToMediaWiki

def test_plain_text():
    text = "This is some plain text."
    expected = text
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    assert result == expected

def test_text_size():
    text = "This is some [[size 180%]]re-sized text[[/size]]."
    expected = "This is some re-sized text."
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    assert result == expected

def test_superscript():
    text = "This is an example of superscript: 2^^nd^^."
    expected = "This is an example of superscript: 2<sup>nd</sup>."
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    assert result == expected

# Internal Link
# =============

def test_internal_link():
    text = "This is some text with a link to an [[[internal page]]]."
    expected = "This is some text with a link to an [[internal page]]."
    instance = WikidotToMediaWiki()
    result, links, _ = instance.convert(text)
    assert result == expected
    assert links == ["internal page"]

def test_internal_link_with_trailing_space():
    text = "This is some text with a link to an [[[internal page ]]]."
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

def test_internal_link_with_alt_text():
    text = "[[[internal page | alternative text]]]"
    expected = "[[internal page|alternative text]]"
    instance = WikidotToMediaWiki()
    result, links, _ = instance.convert(text)
    assert result == expected
    assert links == ["internal page"]

def test_internal_link_with_underscores():
    # Wikidot internal links have underscores converted to hypens 
    text = "[[[internal_page | alternative text]]]"
    expected = "[[internal_page|alternative text]]"
    instance = WikidotToMediaWiki()
    result, links, _ = instance.convert(text)
    assert result == expected
    assert links == ["internal_page"]

# Code Block
# ==========

def test_code():
    text = 'This is a code block: [[code type="python"]]1 + 2 == 3[[/code]]'
    expected = "This is a code block: \n <nowiki>1 + 2 == 3</nowiki>"
    instance = WikidotToMediaWiki()
    result, _, _ = instance.convert(text)
    print("result:", result)
    assert result == expected

# Image
# =====

def test_image():
    text = "This is a link to an image: [[image filename.png]]"
    expected = "This is a link to an image: [[File:filename.png]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_complex_images():
    text = 'This is a link to an image: [[image filename.png size="medium" alt="alternative text"]]'
    expected = "This is a link to an image: [[File:filename.png|500px|alt=alternative text]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_left_aligned_image():
    text = "This is a link to a left-aligned image: [[<image filename.png]]"
    expected = "This is a link to a left-aligned image: [[File:filename.png|left]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_floating_left_image():
    text = "This is a link to a floating-left-aligned image: [[f<image filename.png]]"
    expected = "This is a link to a floating-left-aligned image: [[File:filename.png|left]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_right_aligned_image():
    text = "This is a link to a right-aligned image: [[>image filename.png]]"
    expected = "This is a link to a right-aligned image: [[File:filename.png|right]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_floating_right_image():
    text = "This is a link to a floating-right-aligned image: [[f>image filename.png]]"
    expected = "This is a link to a floating-right-aligned image: [[File:filename.png|right]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_center_aligned_image():
    text = "This is a link to a center-aligned image: [[=image filename.png]]"
    expected = "This is a link to a center-aligned image: [[File:filename.png|center]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_width():
    text = '[[image filename.png width="200px"]]'
    expected = "[[File:filename.png|200px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_square():
    text = '[[image filename.png size="square"]]'
    expected = "[[File:filename.png|75x75px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_thumbnail():
    text = '[[image filename.png size="thumbnail"]]'
    expected = "[[File:filename.png|100px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_small():
    text = '[[image filename.png size="small"]]'
    expected = "[[File:filename.png|240px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_medium():
    text = '[[image filename.png size="medium"]]'
    expected = "[[File:filename.png|500px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_medium640():
    text = '[[image filename.png size="medium640"]]'
    expected = "[[File:filename.png|640px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_large():
    text = '[[image filename.png size="large"]]'
    expected = "[[File:filename.png|1024px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_size_original():
    text = '[[image filename.png size="original"]]'
    expected = "[[File:filename.png]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_height():
    text = '[[image filename.png height="200px"]]'
    expected = "[[File:filename.png|x200px]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_link():
    text = '[[image filename.png link="example.com"]]'
    expected = "[[File:filename.png|link=example.com]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

def test_image_with_alt():
    text = '[[image filename.png alt="some text"]]'
    expected = "[[File:filename.png|alt=some text]]"
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename.png"]

# Gallery
# =======

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

# File
# ====

def test_file():
    text = "This is a file: [[file filename]]"
    expected = "This is a file: [[Media:filename|filename]]" # The alt text is added to improve the MediaWiki formatting
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
        + " when I have a file tag with the same contents [[Media:filename|filename]]."
    )
    instance = WikidotToMediaWiki()
    result, _, linked_files = instance.convert(text)
    print("result:", result)
    assert result == expected
    assert linked_files == ["filename"]
