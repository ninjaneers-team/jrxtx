#!/usr/bin/env python2
from __future__ import print_function

import os
import requests
import shutil
import sys
from pprint import pprint
import re
import errno

output = 'build-download'

LIBRARY_NAME = "librxtxSerial"

REPO = "repos/ninjaneers-team/jrxtx"
BASEURL = "https://api.github.com"


def set_api_key(headers, key):
    headers['Authorization'] = 'token ' + key

if __name__ == "__main__":
    headers = {}
    
    if 'api_key' in os.environ:
        print("API key found in $api_key")
        set_api_key(headers, os.environ['api_key'])
    elif 'TRAVIS_CMD' in os.environ:
        match = re.search(r'api_key="([^"]+)"', os.environ['TRAVIS_CMD'])
        if match:
            print("API key found in $TRAVIS_CMD")
            set_api_key(headers, match.group(1))
        else:
            print("WARNING: API key not found in $TRAVIS_CMD")

    url = ("%s/%s/releases") % (BASEURL, REPO)
    releases = requests.get(url, headers=headers).json()
    
    print("raw releases:")
    pprint(releases)
    print("======")
    
    releases = sorted(releases, key=lambda r: r['created_at'])
    # take the last release
    release = releases[-1]
    if releases is None:
        sys.exit(0)
    print("Using release", release['tag_name'], release['html_url'])
    
    assets = release['assets']
    libs = filter(lambda a: LIBRARY_NAME in a['name'], assets)
    pprint([(l['name'], l['size']) for l in libs])
    
    try:
        os.makedirs('%s' % output)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    for lib in libs:
        r = requests.get(lib['browser_download_url'], headers=headers)
        with open(output + '/' + lib['name'], 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print("written to", f.name, os.stat(f.name).st_size)
