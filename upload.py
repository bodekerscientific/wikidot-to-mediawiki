#!/usr/bin/env python3

import argparse
from pathlib import Path
import warnings

import mediawiki

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("source", help="Directory containing files converted to MediaWiki format")
    parser.add_argument(
        "--secrets", "-s",
        default="SECRETS.py",
        help="File containing the location and credentials of the MediaWiki site"
    )
    parser.add_argument(
        "--only-pages",
        default=False,
        action='store_true',
        help="Only upload pages (don't upload any files)"
    )

    arguments = parser.parse_args()

    # Process secrets file
    secrets_path = Path(arguments.secrets)
    secrets = {}
    exec(secrets_path.read_text(), {}, secrets)
    print("From secrets file:")
    print(f"  Endpoint: {secrets['endpoint']}")
    print(f"  Bot username: {secrets['bot_username']}")

    # Connect to MediaWiki site
    wiki = mediawiki.MediaWiki(secrets["endpoint"], secrets["verify"])
    wiki.login(secrets["bot_username"], secrets["bot_password"])

    # Get pages and files to upload
    source = Path(arguments.source)
    page_paths = sorted(source.glob("*.mktxt"))
    file_paths = sorted((source / "files_to_upload").glob("*"))

    print(f"Found {len(page_paths)} pages")
    print(f"Found {len(file_paths)} files")

    # Upload pages
    for page_path in page_paths:
        print(f"Uploading page {page_path.name}")
        # Hide repeated SSL certificate warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wiki.create_page(
                title=page_path.stem,
                text=page_path.read_text()
            )
    
    if arguments.only_pages:
        print("Not uploading any files as the option --only-pages was set")
        return
        
    # Upload files
    failed_uploads = []
    for file_path in file_paths:
        print(f"Uploading file {file_path.name}")
        try:
            # Hide repeated SSL certificate warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                wiki.upload_file(
                    filename=file_path.name,
                    path=file_path
                )
        except Exception as e:
            print("  Failed")
            failed_uploads.append({
                "filename":file_path.name, 
                "error": str(e)
            })

    # Output list of failures
    if len(failed_uploads) > 0:
        print("The following files failed to upload:")
        for failed_upload in failed_uploads:
            print(f"  {failed_upload['filename']}: {failed_upload['error']}")

if __name__ == '__main__':
    main()
