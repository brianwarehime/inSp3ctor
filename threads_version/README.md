# Threads implementation

If you like more than 10 threas, modify the variable
```
max_consumers = 10
```

This script have progress bar include, if you like to disable modify de variable
```
verbose: bool = True
```

Example:
```bash
# With progress bar
➜  threads_version git:(master) ✗ py prod_consume.py
100% (116 of 116) |############################################| Elapsed Time: 0:00:05 Time:  0:00:05
{"Bucket": {"private": ["http://s3.amazonaws.com/example", "http://example.s3.amazonaws.com"], "public": ["http://flaws.cloud.s3.amazonaws.com"]}, "Object": {"private": ["http://s3.amazonaws.com/example/.ssh/id_rsa.pub~",...], "public": ["http://flaws.cloud.s3.amazonaws.com/hint1.html", ...], "no_exist": ["http://flaws.cloud.s3.amazonaws.com/.bak", ...]}}


# Without progress bar
➜  threads_version git:(master) ✗ py prod_consume.py | jq
{
  "Bucket": {
    "private": [
      "http://s3.amazonaws.com/example",
      "http://example.s3.amazonaws.com"
    ],
    "public": [
      "http://flaws.cloud.s3.amazonaws.com"
    ]
  },
  "Object": {
    "private": [
      "http://s3.amazonaws.com/example/.ssh/id_rsa.pub~",
      ...
    ],
    "public": [
      "http://flaws.cloud.s3.amazonaws.com/hint1.html",
      ...
    ],
    "no_exist": [
      "http://flaws.cloud.s3.amazonaws.com/.ssh/known_host",
      ...
    ]
  }
}
```