#!/usr/bin/env python3

# Copyright 2012 Philipp Klaus
# Part of https://github.com/vLj2/wikidot-to-markdown
# Improved 2016 by Christopher Mitchell
# https://github.com/KermMartian/wikidot-to-markdown
# Improved 2022 by Matthew Walker
# https://github.com/bodekerscientific/wikidot-to-mediawiki

import codecs			## for codecs.open()
import argparse
from pathlib import Path
import shutil
from datetime import datetime

import regex

from wikidot import WikidotToMediaWiki
from page_xml import PageXMLParser


class ConversionController():
    def __init__(self, arguments):
        # self.__input_wiki_file = options.filename
        # self.__output_directory = options.output_dir
        # self.__fill_blog = options.blog
        # self.__create_individual_files = options.individual
        self.__converter = WikidotToMediaWiki()
        self.__args = arguments

    def __get_xml_files(self, source):
        source = Path(source)
        if source.is_dir():
            xml_files = sorted(source.glob("*.xml"))
        elif source.is_file():
            xml_files = [source.parent / (source.stem+".xml")]
        else:
            raise Exception(f"Source ({source}) should be either a directory or file")

        return xml_files

    def __get_text_files(self, source):
        source = Path(source)
        if source.is_dir():
            input_files = sorted(source.glob("*.txt"))
        elif source.is_file():
            input_files = [source]
        else:
            raise Exception(f"Source ({source}) should be either a directory or file")

        print("Input files for pages:")
        for input_file in input_files:
            print(f"  {input_file}")

        return input_files

    def __process_dest(self, dest):
        dest_dir = Path(dest)
        if dest_dir.is_file():
            raise Exception("Destination is not a directory")

        dest_dir.mkdir(parents=True, exist_ok=True)

        print("Output directory:")
        print(f"  {dest_dir}")
        return dest_dir

    def convert(self, source, dest):
        input_files = self.__get_text_files(source)
        xml_files = self.__get_xml_files(source)
        dest_dir = self.__process_dest(dest)
        internal_links_map = {}

        if self.__args.include_associated_xml_files:
            print("Including XML files in directories of associated files.")
        else:
            print("Ignoring XML files in directories of associated files.")

        # Go through the xml files.  Obtain a map from filename to title
        print(f"Processing metadata from XML files:")
        fullname_to_title = {}
        for xml_file in xml_files:
            page_xml_parser = PageXMLParser(xml_file.read_text())
            title = page_xml_parser.title
            #title = regex.sub(" ", "_", title)
            fullname = page_xml_parser.fullname
            print(f"  {fullname}: '{title}'")
            fullname_to_title[fullname] = title

        # Go through the txt files
        for input_file in input_files:
            print(f"Processing page {input_file.stem}")

            # Read associated XML file to obtain the fullname and title.  Hypens and spaces make 
            # it impossible to automatically convert from the fullname to the title.

            f = codecs.open(input_file, encoding='utf-8')
            text = f.read()
            base_filename = input_file.stem
            assert base_filename in fullname_to_title

            file_prefix = base_filename+"__"
            converted_text, internal_links, linked_files = self.__converter.convert(
                text, file_prefix=file_prefix, fullname_to_title=fullname_to_title
            )
            internal_links_map[fullname_to_title[base_filename]] = internal_links

            # Get associated files
            associated_dir = input_file.parent / input_file.stem
            if not associated_dir.is_dir():
                print(f"  Did not find directory of associated files at {associated_dir}")
                associated_files = []
                associated_paths = []
            else:
                associated_paths = sorted(associated_dir.glob("*"))
                associated_files = [f.name for f in associated_paths]

            # Check that all files linked in the text can be found in the associated files
            for linked_file in linked_files:
                if linked_file not in associated_files:
                    print("  Linked file not found in associated dir:", linked_file)

            # Check that all associated files have been linked
            unlinked_associated_files = []
            for associated_file in associated_files:
                if associated_file not in linked_files:
                    xml_file = associated_file.split(".")[-1] == "xml"
                    if xml_file and not self.__args.include_associated_xml_files:
                        continue
                    print("  Associated file not found in linked files:", associated_file)
                    unlinked_associated_files.append(associated_file)

            # Add any unlinked associated files to text
            if len(unlinked_associated_files) > 0:
                appendix = (
                    "\n== Unlinked Associated Files ==\n"
                    + "In Wikidot, there were files associated with this page that were not linked in the text above:\n"
                )
                for unlinked_associated_file in unlinked_associated_files:
                    appendix += "* [[Media:"+file_prefix+unlinked_associated_file+"|"+unlinked_associated_file+"]]\n"
                converted_text = converted_text + appendix
                print("  Added appendix to converted text listing unlinked associated files")

            # Copy all associated files to upload
            upload_dir = dest_dir / "files_to_upload"
            upload_dir.mkdir(parents=True, exist_ok=True)
            existing_files = [f.name for f in sorted(upload_dir.glob("*"))]
            for associated_path in associated_paths:
                xml_file = associated_path.suffix == ".xml"
                if xml_file and not self.__args.include_associated_xml_files:
                    continue
                if associated_path.name in existing_files:
                    message = f"A file with the name {associated_path.name} already exists in {upload_dir}."
                    print("  "+message)
                    # Check if the files are identical
                    associated_bytes = associated_path.read_bytes()
                    upload_bytes = (upload_dir / associated_path.name).read_bytes()
                    if associated_bytes == upload_bytes:
                        print("  But the two files are identical.")
                        continue
                    else:
                        print("  And the two files are different.")
                        raise Exception(message)

                upload_path = upload_dir / (file_prefix+associated_path.name)
                print(f"  Copying {associated_path} to {upload_path}")
                shutil.copy(associated_path, upload_path)

            # Write converted text
            output_file = dest_dir / (fullname_to_title[base_filename]+'.mktxt')
            print(f"  Writing {output_file}")
            self.write_unicode_file(output_file, converted_text)

        # Find orphaned pages
        orphaned_pages = {page:True for page in internal_links_map.keys()}
        for _, links in internal_links_map.items():
            for link in links:
                if link in orphaned_pages:
                    orphaned_pages[link] = False

        # Create page of pages that were processed, highlighting orphaned pages
        processed_pages = (
            "[https://github.com/bodekerscientific/wikidot-to-mediawiki Wikidot-to-MediaWiki] ran at "
            + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.  It processed the following {len(input_files)} pages:\n"
        )
        any_orphaned = False
        pages = sorted(orphaned_pages.keys(), key=str.lower)
        for page in pages:
            processed_pages += f"* [[{page}]]"
            if orphaned_pages[page]:
                processed_pages += " *"
                any_orphaned = True
            processed_pages += "\n"
        if any_orphaned:
            processed_pages += "\n<nowiki>*</nowiki> Orphaned page (that is, no pages link to the page).\n"

        print("Writing report of conversion")
        output_file = dest_dir / "Wikidot_to_MediaWiki_report.mktxt"
        self.write_unicode_file(output_file, processed_pages)

        print(internal_links_map)


    def write_unicode_file(self, path_to_file, content):
        try:
            out_file = codecs.open(path_to_file,encoding='utf-8', mode='w')
            out_file.write(content)
        except:
            print("Error on writing to file %s." % path_to_file)

def main():
    """ Main function called to start the conversion."""
    parser = argparse.ArgumentParser()

    parser.add_argument('source', help="File or directory containing source files from Wikidot site")
    parser.add_argument('dest', help="Directory to output files converted to MediaWiki format")
    parser.add_argument(
        "-x",
        "--include-associated-xml-files",
        default=False,
        action='store_true',
        help="Include any XML files in the files associated with source files"
    )
    arguments = parser.parse_args()

    converter = ConversionController(arguments)
    converter.convert(arguments.source, arguments.dest)

if __name__ == '__main__':
    main()
