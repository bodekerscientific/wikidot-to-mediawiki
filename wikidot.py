#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# Copyright 2012 Philipp Klaus
# Part of https://github.com/vLj2/wikidot-to-markdown
# Improved 2016 by Christopher Mitchell
# https://github.com/KermMartian/wikidot-to-markdown
# Improved 2022 by Matthew Walker
# https://github.com/bodekerscientific/wikidot-to-mediawiki

from turtle import title
import regex as re
import uuid			## to generate random UUIDs using uuid.uuid4()

class WikidotToMediaWiki():
    def __init__(self):
        # regex for URL found on http://regexlib.com/REDetails.aspx?regex_id=501
        self.url_regex = r"(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\?\'\\\+&amp;%\$#\=~_\-]+))*[/]?"

        self.static_replacements = { '[[toc]]': '', # no equivalent for table of contents in Markdown
                                   }
        self.regex_replacements = { r'([^:])//([\s\S ]*?[^:])//': r"\1''\2''", # italics
                                    r'([^:])\*\*([\s\S ]*?)\*\*': r"\1'''\2'''", # bold
                                    r'([^:])\[!--([\s\S ]*?)--\]': r"\1<!--\2-->", # comments
                                    r'([^:])__([\s\S ]*?)__': r"\1'''\2'''", # underlining → bold
                                    #r'([^:]){{([\s\S ]*?)}}': r'\1`\2`', # inline monospaced text
                                    r'\^\^([\S\s]*?)\^\^': r'<sup>\1</sup>', # superscript
                                    r'\[\[size\s*\S*?\]\]': r'', # ignore text sizing
                                    r'\[\[/size\s*?\]\]' : r'',  # ignore text sizing
                                  }
        self.regex_split_condition = r"^\+ ([^\n]*)$"

    def convert(self, text, file_prefix="", fullname_to_title={}):
        text = '\n'+text+'\n'# add embed in newlines (makes regex replaces work better)
        # first we search for [[code]] statements as we don't want any replacement to happen inside those code blocks!
        code_blocks = dict()
        code_blocks_found = re.findall(re.compile(r'(\[\[code( type="([\S]+)")?\]\]([\s\S ]*?)\[\[/code\]\])',re.MULTILINE), text)
        for code_block_found in code_blocks_found:
            tmp_hash = str(uuid.uuid4())
            text = text.replace(code_block_found[0],tmp_hash,1) # replace code block with a hash - to fill it in later
            code_blocks[tmp_hash] = code_block_found[-1]
        for search, replacement in self.static_replacements.items():
            text = text.replace(search,replacement,1)
            
        # search for any of the simpler replacements in the dictionary regex_replacements
        for s_reg, r_reg in self.regex_replacements.items():
            text = re.sub(re.compile(s_reg,re.MULTILINE),r_reg,text)
        # TITLES -- replace '+++ X' with '=== X ==='
        for titles in re.finditer(r"^(\++)([^\n]*)$", text, re.MULTILINE):
            header = ("=" * len(titles.group(1)))
            text = text.replace(titles.group(0), header + (titles.group(2) + " ") + header)
        # LISTS(*) -- replace '  *' with '***' and so on         
        for stars in re.finditer(r"^([ \t]+)\*", text, re.MULTILINE):
            text = text[:stars.start(1)] + ("*" * len(stars.group(1))) + text[stars.end(1):]
        # LISTS(#) -- replace '  #' with '###' and so on
        for hashes in re.finditer(r"^([ \t]+)\*", text, re.MULTILINE):
            text = text[:hashes.start(1)] + ("#" * len(hashes.group(1))) + text[hashes.end(1):]

        # Internal links -- replace [[[internal link]]] with [[internal link]], informed 
        # by mapping from fullname to title
        lower_title_to_case_sensitive_title = {
            title.lower(): title
            for title in fullname_to_title.values()
        }

        def convert_internal_link(link: str):
            # Trim whitespace at either end
            link = link.strip()
            # Convert underscores and at-signs to hypens (because that's what Wikidot did)
            fullname = re.sub(r"[_@]", r"-", link)
            # Convert link to lower case (because that's what Wikidot did)
            fullname = fullname.lower()
            if fullname in fullname_to_title:
                return fullname_to_title[fullname]
            else:
                # Check if link references page title rather than its fullname
                #title = re.sub(" ", "_", link)
                lower_title = link.lower() # Wikidot seems to be case-insensitive
                if lower_title in lower_title_to_case_sensitive_title:
                    return lower_title_to_case_sensitive_title[lower_title]
            print(f"  Failed to find page given the link '{link}'")
            return link

        internal_links = []
        for inlink in re.finditer(r"\[\[\[([\s\S]*?)\]\]\]", text):
            inlink_contents = inlink.group(1)
            # Check for existance of alternative text
            pattern = re.compile(r"([\S\s]*?)[\s]*\|[\s]*([\S\s]*?)")
            match = pattern.fullmatch(inlink_contents)
            if match is not None:
                # Contents contains alternative text
                internal_page = convert_internal_link(match.group(1))
                alt_text = match.group(2)
                replacement_contents = f"[[{internal_page}|{alt_text}]]"
            else:
                # Contents must be only the name of the internal page
                internal_page = convert_internal_link(inlink_contents)
                replacement_contents = f"[[{internal_page}]]"
            text = text.replace(inlink.group(0), replacement_contents)
            internal_links.append(internal_page)

        # Image
        linked_files = []
        for image in re.finditer(r"\[\[(f?[=<>]?)image\s*([\S\s]*?)\s*\]\]", text):
            image_format = image.group(1)
            image_contents = image.group(2)

            # Process the horizontal alignment of the image
            options = []
            if image_format == "<" or image_format == "f<":
                options.append("left")
            if image_format == ">" or image_format == "f>":
                options.append("right")
            if image_format == "=":
                options.append("center")
            
            # Process any attributes
            filename = image_contents
            for attribute in re.finditer(r"(\S*?)=\"([\S\s]*?)\"", image_contents, re.MULTILINE):
                key = attribute.group(1)
                value = attribute.group(2)
                if key == "width":
                    options.append(value)
                if key == "height":
                    options.append("x"+value)
                if key == "size":
                    if value == "square":
                        options.append("75x75px")
                    if value == "thumbnail":
                        options.append("100px")
                    if value == "small":
                        options.append("240px")
                    if value == "medium":
                        options.append("500px")
                    if value == "medium640":
                        options.append("640px")
                    if value == "large":
                        options.append("1024px")
                if key == "link":
                    options.append(f"link={value.lstrip()}")
                if key == "alt":
                    options.append(f"alt={value.lstrip()}")
                filename = re.sub(attribute.group(0), "", filename)

            original_filename = filename.strip()
            filename = file_prefix + original_filename
            file_contents = "|".join([filename] + options)
            text = text.replace(image.group(0), "[[File:" + file_contents + "]]")
            linked_files.append(original_filename)

        # Gallery
        for gallery in re.finditer(r"\[\[gallery[ \S]*?\]\]([\S\s ]*)\[\[/gallery\]\]", text, re.MULTILINE):
            replacement_gallery = "<gallery>\n"
            gallery_content = gallery.group(1)
            for filename_match in re.finditer(r"^: ([\S]*)", gallery_content, re.MULTILINE):
                original_filename = filename_match.group(1)
                filename = file_prefix + original_filename
                replacement_gallery += filename + "\n"
                linked_files.append(original_filename)
            replacement_gallery += "</gallery>"
            text = text.replace(gallery.group(0), replacement_gallery)

        # File
        for file in re.finditer(r"\[\[file[\s]*([\S\s]*?)[\s]*\]\]", text, re.MULTILINE):
            file_contents = file.group(1)
            # Check for existance of alternative text
            pattern = re.compile(r"([\S\s]*?)[\s]*\|[\s]*([\S\s]*?)")
            match = pattern.fullmatch(file_contents)
            if match is not None:
                # Contents contains alternative text
                original_filename = match.group(1)
                filename = file_prefix + original_filename
                alt_text = match.group(2)
                replacement_contents = f"[[Media:{filename}|{alt_text}]]"
            else:
                # Contents must be only the filename
                original_filename = file_contents
                filename = file_prefix + original_filename
                replacement_contents = f"[[Media:{filename}|{filename}]]"
            text = text.replace(file.group(0), replacement_contents)
            linked_files.append(original_filename)

        # START TABLE
        for table in re.finditer(r"\[\[table([\s\S ]*?)\]\]", text):
            #text = text.replace(table.group(0), "{|" + table.group(1))
            text = text.replace(table.group(0), "{|")
        # START ROW
        for row in re.finditer(r"\[\[row([\s\S ]*?)\]\]", text):
            #text = text.replace(row.group(0), "|-" + row.group(1))
            text = text.replace(row.group(0), "|-")
        # START CELL
        for cell in re.finditer(r"\[\[cell([\s\S ]*?)\]\]", text):
            #text = text.replace(cell.group(0), "|" + cell.group(1))
            text = text.replace(cell.group(0), "|")
        # ENDS
        for end in re.finditer(r"\[\[/([\s\S ]*?)\]\]", text):
            token = end.group(1)
            if token == "table":
                text = text.replace(end.group(0), "|}")
            elif token == "row":
                # end row tabs are not necessary in mediawiki
                text = text.replace(end.group(0), "")
            elif token == "cell":
                # end cell tabs are not necessary in mediawiki
                text = text.replace(end.group(0), "")

        # Substitute back our code blocks
        for tmp_hash, code in code_blocks.items():
            code = "\n <nowiki>"+code+"</nowiki>"
            text = text.replace(tmp_hash, code, 1)

        # Process color corrections
        startpos = 0
        while -1 != startpos:
            startpos = text.find("##", startpos)
            pipepos = text.find("|", startpos + 2)
            endpos = text.find("##", startpos + 2)
            if startpos != -1 and pipepos != -1 and endpos != -1 and endpos > pipepos:
                color = text[startpos + 2 : pipepos].strip()
                colored = text[pipepos + 1 : endpos].strip()
                text = text[: startpos] + "<span style=\"color:" + color + "\">" + colored + \
                       "</span>" + text[endpos + 2 :]
                startpos = endpos
                
        # Process math corrections
        startpos = 0
        while -1 != startpos:
            startpos = text.find("[[$", startpos)
            endpos = text.find("$]]", startpos)
            if startpos != -1 and endpos != -1:
                mathtext = text[startpos + 3 : endpos].strip()
                text = text[: startpos] + "<math>" + mathtext + "</math>" + text[endpos + 3 :]
                startpos = endpos

        # Process table corrections
        startpos = 0
        while -1 != startpos:
            startpos = text.find("\n||", startpos)
            if startpos == -1:
                break

            # Find end of table
            endpos = text.find("\n", startpos + 3)
            while endpos < len(text) - 3 and "||" == text[endpos + 1: endpos + 3]:
                endpos = text.find("\n", endpos + 3)

            # Found bounds of text chunk: reformat table
            fixup = text[startpos + 1 : endpos].replace("||~", "!!")
            fixup = fixup.split("\n")
            fixout = ["", "{| class=\"wikitable\""]
            for i in range(len(fixup)):
                if fixup[i][0 : 2] == "||" or fixup[i][0 : 2] == "!!":
                    out = fixup[i].strip()[1 : ]
                    fixout.append(out[ : -2 if out[-2 : ] in ["||", "!!"] else 0])
                else:
                    message = "Failed to parse item %d/%d: '%s'" % (i, len(fixup), fixup[i])
                    raise Exception(message)
                fixout.append("|}" if i == len(fixup) - 1 else "|-")

            # Construct output table text
            fullout = "\n".join(fixout)
            text = text[ : startpos] + fullout + text[endpos : ]
            startpos = startpos + len(fullout)

        # Repair multi-newlines
        text = re.sub(r"\n\n+", "\n\n", text, re.M)

        # Repair starting newlines
        text = text.strip()

        return text, internal_links, linked_files
