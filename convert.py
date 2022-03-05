#!/usr/bin/env python

# Copyright 2012 Philipp Klaus
# Part of https://github.com/vLj2/wikidot-to-markdown
# Improved 2016 by Christopher Mitchell
# https://github.com/KermMartian/wikidot-to-markdown

from wikidot import WikidotToMarkdown ## most important here

import sys				## for sys.exit()
import os				## for os.makedirs()
import optparse			## for optparse.OptionParser()
import codecs			## for codecs.open()
import datetime as dt	## for dt.datetime() and dt.datetime.now()
import time				## for time.sleep()

DEFAULT_OUTPUT_DIR = "output"
SLEEP_TIME = 0 # seconds to sleep after each post sent to the blog (if you use your own server, set this to 0)

class ConversionController(object):
    def __init__(self, options):
        self.__input_wiki_file = options.filename
        self.__output_directory = options.output_dir
        self.__fill_blog = options.blog
        self.__create_individual_files = options.individual
        self.__converter = WikidotToMarkdown()

    def __prepare_output_dir(self):
        try:
            os.makedirs(self.__output_directory)
        except OSError as ex:
            print("Could not create output folder "+self.__output_directory+".")
            if ex.errno == os.errno.EEXIST: print("It already exists.")
            else: 
                print("Error %i: %s" % (ex.errno, str(ex)))
                sys.exit(1)

    def convert(self):
        self.__prepare_output_dir()
        f = codecs.open(self.__input_wiki_file, encoding='utf-8')
        text = f.read()
        base_filename = os.path.splitext(os.path.basename(self.__input_wiki_file))[0]
        
        # write the complete files to the output directory:
        complete_text = self.__converter.convert(text)
        self.write_unicode_file("%s/%s" % (self.__output_directory, base_filename+'.mktxt'),complete_text)

        # now handle the texts split to little junks:
        if self.__create_individual_files:
            parts = self.__converter.split_text(text)
            if len(parts) < 2: return # we need at least 2 entries (the first part is trashed and one part with content!)
            i=0
            for text_part in parts:
                text_part =  self.__converter.convert(text_part)
                i += 1
                if i == 1:
                    print("\nAttention! We skip the first output part (when splitting the text into parts):\n\n%s" % text_part)
                    continue
                if self.__create_individual_files:
                    self.write_unicode_file(
                        os.path.join(self.__output_directory, "%s/%i%s" % (i, '.mktxt')), 
                        text_part
                    )
                lines = text_part.split("\n")
                if self.__fill_blog:
                    title = lines[0].replace("# ","")
                    content = string.join(lines[1:],'\n')
                    date = dt.datetime(start[0],start[1],start[2], 17, 11, 11) + dt.timedelta(int((i-2)*gradient))
                    wprb.post_new(title, content,[],'','private',date)
                    time.sleep(SLEEP_TIME)

    def write_unicode_file(self, path_to_file, content):
        try:
            out_file = codecs.open(path_to_file,encoding='utf-8', mode='w')
            out_file.write(content)
        except:
            print("Error on writing to file %s." % path_to_file)

def main():
    """ Main function called to start the conversion."""
    p = optparse.OptionParser(version="%prog 1.0")

    # set possible CLI options
    p.add_option('--save-junks-to-blog', '-b', action="store_true", help="save the individual files as blog posts (only relevant if -s set)", default=False, dest="blog")
    p.add_option('--save-individual', '-s', action="store_true", help="save individual files for every headline", default=False, dest="individual")
    p.add_option('--input-file', '-f', metavar="INPUT_FILE", help="Read from INPUT_FILE.", dest="filename")
    p.add_option('--output-dir', '-o', metavar="OUTPUT_DIRECTORY", help="Save the converted files to the OUTPUT_DIRECTORY.", dest="output_dir")

    # parse our CLI options
    options, arguments = p.parse_args()
    if options.filename == None:
        p.error("No filename for the input file set. Have a look at the parameters using the option -h.")
        sys.exit(1)
    if options.output_dir == None:
        options.output_dir = raw_input('Please enter an output directory for the converted documents [%s]: ' % DEFAULT_OUTPUT_DIR)
        if options.output_dir == "": options.output_dir = DEFAULT_OUTPUT_DIR

    converter = ConversionController(options)
    converter.convert()

if __name__ == '__main__':
    main()
