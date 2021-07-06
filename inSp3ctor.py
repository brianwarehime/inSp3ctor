#!/usr/bin/env python

"""

    _      _____      _____      __            
   (_)___ / ___/____ |__  /_____/ /_____  _____
  / / __ \\__ \/ __ \ /_ </ ___/ __/ __ \/ ___/
 / / / / /__/ / /_/ /__/ / /__/ /_/ /_/ / /    
/_/_/ /_/____/ .___/____/\___/\__/\____/_/     
            /_/                                

Created by Brian Warehime @nullsecure
08/10/2017

Tool to search for public bucket/objects for a given name.

Todo:
- Save results to disk
- Support for reading multiple root names
"""

import argparse
from bs4 import BeautifulSoup
import os
import re
import requests
import sys
import json

try:
    from awsauth import S3Auth
except ImportError:
    pass

from datetime import datetime

results = dict()


class bcolors:
    WHITE = '\033[40m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def parse_response(xml_response):
    """
    Get the content of the HTML page for the bucket and return
    the redirected page if given a 301 status

    Args:
        xml_response (str): The HTML content from an s3 bucket

    Returns:
        String of the redirected S3 bucket
    """
    y = BeautifulSoup(xml_response, "html.parser")
    return y.error.endpoint.string


def check_object_status(xml_response, site):
    """
    Get the content of the HTML page for the bucket and return
    the status of objects contained in the bucket

    Args:
        xml_response (str): The HTML content from an s3 bucket
        site (str): URL of the s3 bucket

    Returns:
        Object status
    """
    y = BeautifulSoup(xml_response, "html.parser")
    object_keys = y.findAll('key')
    for key in object_keys:
        bucket_checker(site.rstrip() + "/" + key.get_text(), "Object")


def check_response(status_code, word, content, s3_type):
    """
    Formats the response code based on status code returned
    from s3 bucket, and changes color depending on the response.

    Args:
        status_code (int): The HTTP response code from the s3 bucket
        word (str): The name of the s3 bucket to check
        content (str): The HTML content from the s3 bucket

    Returns:
        None
    """
    redirect = ''
    if args.p:
        if status_code == 200:
            log_objects(word.rstrip(), s3_type, 'public')
            if args.o:
                check_object_status(content, word)
    else:
        if status_code == 200:
            log_objects(word.rstrip(), s3_type, 'public')
            if args.o:
                check_object_status(content, word)
        elif status_code == 403:
            log_objects(word.rstrip(), s3_type, 'private')
        elif status_code == 301:
            redirect = parse_response(content)
            log_objects(word.rstrip(), s3_type, 'redirect', redirect)
        else:
            log_objects(word.rstrip(), s3_type, 'no_exist', redirect)
    if outfile:
        write_header = False
        if not os.path.isfile(outfile):
            write_header = True
        with open(outfile, 'a') as f:
            if write_header:
                f.write('status_code,url,bucket_type,redirected_url\n')
            f.write(str(status_code) + ',' + str(word.encode('utf-8')) + ',' +
                    s3_type + ',' + redirect + "\n")


def log_objects(text, s3_type, state, redirect=None):
    if args.j:
        if redirect:
            results[s3_type].setdefault(
                state, []).append(f"{text} -> {redirect}")
        else:
            results[s3_type].setdefault(state, []).append(text)
    else:
        if state == 'public':
            print(bcolors.OKGREEN +
                  f"[*] {s3_type} is public [{text}]" + bcolors.ENDC)
        elif state == 'private':
            print(bcolors.WARNING +
                  f"[!] {s3_type} is marked private [{text}]" + bcolors.ENDC)
        elif state == 'redirect':
            print(
                bcolors.FAIL + f"[>] {s3_type} has a redirect [{text}] Redirected here - [{redirect}]" + bcolors.ENDC)
        else:
            print(
                f"[-] {s3_type} does not exist or cannot list [{text}]")


def print_verbose(text):
    if args.v:
        print(text)


def print_header():
    """
    Prints a formatted header

    Args:
        None

    Returns:
        None
    """
    print(bcolors.ENDC + bcolors.WHITE + bcolors.OKBLUE)
    print("            _____      _____      __            ".ljust(80))
    print("    (_)___ / ___/____ |__  /_____/ /_____  _____".ljust(80))
    print("   / / __ \\__ \/ __ \ /_ </ ___/ __/ __ \/ ___/".ljust(80))
    print("  / / / / /__/ / /_/ /__/ / /__/ /_/ /_/ / /    ".ljust(80))
    print(" /_/_/ /_/____/ .___/____/\___/\__/\____/_/     ".ljust(80))
    print("             /_/                                ".ljust(80))
    print(" ".ljust(80))
    print("  AWS S3 Bucket Finder                          ".ljust(80))
    print("  Brian Warehime @nullsecure".ljust(80))
    print(" ".ljust(80) + bcolors.ENDC)


def bucket_checker(word, s3_type):
    """
    Grabs the response from the bucket and checks the response code
    to determine if the bucket is public or private

    Args:
        word (str): The bucket name to check

    Returns:
        None
    """
    if s3_type == "Object":
        if args.a:
            checker = requests.head(word.rstrip(), auth=S3Auth(ACCESS_KEY,
                                                               SECRET_KEY))
        else:
            checker = requests.head(word.rstrip())
    if s3_type == "Bucket":
        if args.a:
            checker = requests.get(word.rstrip(), auth=S3Auth(ACCESS_KEY,
                                                              SECRET_KEY))
        else:
            checker = requests.get(word.rstrip())
    check_response(checker.status_code, word, checker.content, s3_type)


def grab_wordlist(inputfile):
    """
    Grabs each line of a given wordlist

    Args:
        inputfile (str): The name of the text file with bucket names

    Returns:
        None
    """
    with open(inputfile) as f:
        for line in f:
            bucket_checker(line.rstrip(), "Bucket")


def add_permutations(word):
    """
    Given a root word, append a permutation of common terms to view
    if they are created or not.

    Args:
        word (str): The root word to append permutations to

    Returns:
        None
    """
    # Check the base word too.
    if len(word) < 64:
        bucket_checker("http://" + word.rstrip() +
                       ".s3.amazonaws.com", "Bucket")
        bucket_checker("http://s3.amazonaws.com/" + word.rstrip(), "Bucket")
    with open('permutations.txt') as f:
        for line in f:
            permutation = word.rstrip() + line.rstrip()
            # Max lengthfor S3 Bucket names is 63 characters.
            if len(permutation) < 64:
                bucket_checker("http://" + permutation + ".s3.amazonaws.com",
                               "Bucket")
                bucket_checker("http://s3.amazonaws.com/" + permutation,
                               "Bucket")
            else:
                print(Back.RED + '[!] ' + permutation + ' is ' + str(len(word))
                      + 'characters. This an illegal length for a S3 Bucket.' +
                      Style.RESET_ALL)


def batch_checker(inputfile):
    """
    Grabs each line of a given wordlist and run some local
    permutations if the line contains whitespace or &'s.

    Args:
        inputfile (str): The name of the text file with bucket names

    Returns:
        None
    """
    with open(inputfile) as f:
        bad_chars = re.compile(r"[.*$<,>?!'()\"\\/]|[-+$]")
        sub_chars = re.compile(r"[&\+]")
        for word in f:
            if bad_chars.search(word):
                word = bad_chars.sub('', word)
            if sub_chars.search(word):
                # We could get away with having '_': {'and'} not being a set,
                # but then we would have to run another check for if type(i)
                # is set() and it would just add way more unnecessary code.
                base_permutations = {
                    '-': {'and', '-'},
                    '_': {'and'},
                    '': {'and', ''}
                }
                # '+' can mean either 'and' or 'plus', account for both.
                if '+' in word:
                    base_permutations.update({
                        '-': {'plus', '-'},
                        '_': {'plus'},
                        '': {'plus', ''}
                    })
                words_run = []
                for k, v in base_permutations.items():
                    for i in set(v):
                        word_fixed = re.sub(r"[^\S\n]+", str(k),
                                            sub_chars.sub(str(i), word)).rstrip()
                        if '-+' in word_fixed:
                            word_fixed = re.sub('-+', '-', word_fixed)
                        if '---' in word_fixed:
                            word_fixed = re.sub('---', '-', word_fixed)
                        if 'and' not in i and word_fixed.endswith(i):
                            word_fixed = word_fixed.rstrip(i)
                        if word_fixed and word_fixed not in words_run:
                            add_permutations(word_fixed)
                            words_run.append(word_fixed)
            elif re.search(r"[^\S\n]+", word):
                base_permutations = ['-', '_', '']
                for base_permutation in base_permutations:
                    word_fixed = re.sub(
                        r"[^\S\n]+", str(base_permutation), word)
                    add_permutations(word_fixed)
            else:
                add_permutations(word)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='AWS s3 Bucket Permutation Checker')
    parser.add_argument(
        '-w', help='Specify list of buckets to check from wordlist', metavar='wordlist', default='')
    parser.add_argument(
        '-n', help='Specify the root name to use, i.e. google, amazon', metavar='root', default='')
    parser.add_argument(
        '-o', help='Check objects in a public s3 bucket if they are available', action='store_true')
    parser.add_argument('-c', help='Write results to csv', action='store_true')
    parser.add_argument(
        '-a', help='Use AWS Credentials to authenticate the request', action='store_true')
    parser.add_argument(
        '-p', help='Only show buckets/objects that are public in the results', action='store_true')
    parser.add_argument(
        '-b', help='Specify filename containing words to apply permutations to', metavar='batch', default='')
    parser.add_argument('-j', help='JSON output', action='store_true')
    parser.add_argument('-t', help='Do not print banner',
                        action='store_false', default=True)
    parser.add_argument('-v', help='Verbose', action='store_true')
    args = parser.parse_args()

    outfile = ''

    if args.t:
        print_header()

    if args.a:
        ACCESS_KEY = ''
        SECRET_KEY = ''
        if len(ACCESS_KEY) == 0:
            print("[!] Need to supply ACCESS_KEY and SECRET_KEY in this file.")
            sys.exit(1)

    if not args.n and not args.w and not args.b:
        print_verbose("[!] Need to specify root name to use")
        parser.print_help()
        sys.exit(1)

    if args.w:
        print_verbose("[!] Reading s3 bucket names from " + args.w)
        if args.c:
            outfile = str(os.path.splitext(os.path.basename(args.w))[0] + '-' +
                          datetime.now().strftime("%H-%M-%S") + ".csv")
        grab_wordlist(args.w)

    if args.n:
        print_verbose("[!] Applying permutations to " + args.n)
        if args.c:
            outfile = str(args.n + '-' + datetime.now().strftime("%H-%M-%S") +
                          ".csv")
        add_permutations(args.n)

    if args.b:
        print_verbose("[!] Applying permutations to " + args.b)
        if args.c:
            outfile = str(os.path.splitext(os.path.basename(args.b))[0] + '-' +
                          datetime.now().strftime("%H-%M-%S") + ".csv")
        batch_checker(args.b)

    if args.j:
        print(json.dumps(results))
