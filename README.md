# inSp3ctor
AWS S3 Bucket/Object Finder

```
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
```

## How To Use

You can either use a pre-made wordlist containing all the buckets/objects you want to check or supply a root name, and let inSp3ctor add in common permutations to the bucket name to find different variations. 

### Example

If you wanted to look for any information for `example`, you'd run `python inSp3ctor.py -n example`, you can supply the argument `-o` if you want to check the status of the objects contained in the public buckets.

```[!] Applying permutations to example
[!] Bucket is marked private [http://example-dev.s3.amazonaws.com]
[>] Bucket has a redirect [http://s3.amazonaws.com/example-dev] Redirected here - [example-dev.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://example-prod.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-prod]
[-] Bucket does not exist or cannot list [http://example-production.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-production]
[-] Bucket does not exist or cannot list [http://example-tmp.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-tmp]
[-] Bucket does not exist or cannot list [http://example-tmp-logs.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-tmp-logs]
[!] Bucket is marked private [http://example-logs.s3.amazonaws.com]
[!] Bucket is marked private [http://s3.amazonaws.com/example-logs]
[-] Bucket does not exist or cannot list [http://example-splunk.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-splunk]
[-] Bucket does not exist or cannot list [http://example-github.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-github]
[-] Bucket does not exist or cannot list [http://example-keys.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-keys]
[-] Bucket does not exist or cannot list [http://example-secret.s3.amazonaws.com]
[-] Bucket does not exist or cannot list [http://s3.amazonaws.com/example-secret]
[!] Bucket is marked private [http://example-data.s3.amazonaws.com]
[>] Bucket has a redirect [http://s3.amazonaws.com/example-data] Redirected here - [example-data.s3.amazonaws.com]```
