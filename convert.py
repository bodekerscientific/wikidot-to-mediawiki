#!/usr/bin/env python

# Copyright 2012 Philipp Klaus
# Part of https://github.com/vLj2/wikidot-to-markdown
# Improved 2016 by Christopher Mitchell
# https://github.com/KermMartian/wikidot-to-markdown
# Improved 2022 by Matthew Walker
# https://github.com/bodekerscientific/wikidot-to-mediawiki

import sys				## for sys.exit()
import os				## for os.makedirs()
import codecs			## for codecs.open()
import datetime as dt	## for dt.datetime() and dt.datetime.now()
import time				## for time.sleep()
import argparse
from pathlib import Path

from wikidot import WikidotToMediaWiki


class ConversionController():
    def __init__(self, arguments):
        # self.__input_wiki_file = options.filename
        # self.__output_directory = options.output_dir
        # self.__fill_blog = options.blog
        # self.__create_individual_files = options.individual
        self.__converter = WikidotToMediaWiki()
        self.__args = arguments

    def __process_source(self, source):
        source = Path(source)
        if source.is_dir():
            input_files = sorted(source.glob("*.txt"))
        elif source.is_file():
            input_files = [source]
        else:
            raise Exception(f"Source ({source}) should be either a directory or file")

        print("Input files:")
        for input_file in input_files:
            print(f"  {input_file}")

        return input_files

    def __process_dest(self, dest):
        dest_dir = Path(dest)
        if not dest_dir.is_dir():
            raise Exception("Destination is not a directory")

        dest_dir.mkdir(parents=True, exist_ok=True)

        print("Output directory:")
        print(f"  {dest_dir}")
        return dest_dir

    def convert(self, source, dest):
        input_files = self.__process_source(source)
        dest_dir = self.__process_dest(dest)
        internal_links_map = {}

        for input_file in input_files:
            print(f"Processing {input_file}")
            f = codecs.open(input_file, encoding='utf-8')
            text = f.read()
            base_filename = input_file.stem

            converted_text, internal_links, linked_files = self.__converter.convert(text)
            internal_links_map[base_filename] = internal_links
            output_file = dest_dir / (base_filename+'.mktxt')
            self.write_unicode_file(output_file, converted_text)

            # Attempt to find the linked files
            associated_dir = input_file.parent / input_file.stem
            assert associated_dir.is_dir()
            associated_files = sorted(associated_dir.glob("*"))
            associated_files = [f.name for f in associated_files]
            # Check that all files linked in the text can be found in the associated files
            for linked_file in linked_files:
                if linked_file not in associated_files:
                    print("  Linked file not found in associated dir:", linked_file)
            # Check that all associated files have been linked
            for associated_file in associated_files:
                if associated_file not in linked_files:
                    xml_file = associated_file.split(".")[-1] == "xml"
                    if xml_file and self.__args.ignore_associated_xml_files:
                        continue
                    print("  Associated file not found in linked files:", associated_file)

        print("Internal links:")
        print(internal_links_map)

    def write_unicode_file(self, path_to_file, content):
        try:
            out_file = codecs.open(path_to_file,encoding='utf-8', mode='w')
            out_file.write(content)
        except:
            print("Error on writing to file %s." % path_to_file)

def main():
    """ Main function called to start the conversion."""
    #p = optparse.OptionParser(version="%prog 1.0")
    parser = argparse.ArgumentParser()

    # set possible CLI options
    # p.add_option('--save-junks-to-blog', '-b', action="store_true", help="save the individual files as blog posts (only relevant if -s set)", default=False, dest="blog")
    # p.add_option('--save-individual', '-s', action="store_true", help="save individual files for every headline", default=False, dest="individual")
    # p.add_option('--input-file', '-f', metavar="INPUT_FILE", help="Read from INPUT_FILE.", dest="filename")
    # p.add_option('--input-dir', '-d', metavar="INPUT_FILE", help="Read from INPUT_FILE.", dest="filename")
    # p.add_option('--output-dir', '-o', metavar="OUTPUT_DIRECTORY", help="Save the converted files to the OUTPUT_DIRECTORY.", dest="output_dir")
    parser.add_argument('source', help="File or directory containing source files from Wikidot site")
    parser.add_argument('dest', help="Directory to output files converted to MediaWiki format")
    parser.add_argument(
        "-i",
        "--ignore-associated-xml-files", 
        action='store_true',
        help="Ignore any XML files in the files associated with source files"
    )
    arguments = parser.parse_args()

    # parse our CLI options
    # options, arguments = p.parse_args()
    # if options.filename == None:
    #     p.error("No filename for the input file set. Have a look at the parameters using the option -h.")
    #     sys.exit(1)
    # if options.output_dir == None:
    #     options.output_dir = raw_input('Please enter an output directory for the converted documents [%s]: ' % DEFAULT_OUTPUT_DIR)
    #     if options.output_dir == "": options.output_dir = DEFAULT_OUTPUT_DIR

    converter = ConversionController(arguments)
    converter.convert(arguments.source, arguments.dest)

if __name__ == '__main__':
    main()
