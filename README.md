# inSp3ctor
AWS S3 Bucket/Object Finder

   _      ____     ____     __
  (_)__  / __/__  |_  /____/ /____  ____
 / / _ \_\ \/ _ \_/_ </ __/ __/ _ \/ __/
/_/_//_/___/ .__/____/\__/\__/\___/_/
          /_/

  AWS S3 Bucket Finder
  Brian Warehime @nullsecure


[!] Need to specify root name to use
usage: inSp3ctor.py [-h] [-w wordlist] [-n root] [-o]

AWS s3 Bucket Permutation Checker

optional arguments:
  -h, --help   show this help message and exit
  -w wordlist  Specify explicit wordlist to use for all bucket checking
  -n root      Specify the root name to use, i.e. google, amazon
  -o           Check objects in a public s3 bucket if they are available

## How To Use

You can either use a pre-made wordlist containing all the buckets/objects you want to check or supply a root name, and let inSp3ctor add in common permutations to the bucket name to find different variations. 

### Example

If you wanted to look for any information for nullsecure.org, you'd run `python inSp3ctor.py -n nullsecure`, you can supply the argument `-o` if you want to check the status of the objects contained in the public buckets.