This directory contains a number of archives used for testing of `box add`
inspection functionality. For different providers, these box archives contain
a single file `metadata.json`. The different box files targetet at the 
virtualbox provider for example, contain a single json file with the contents:
```
{
    "provider": "virtualbox"
}
```

Vagrant makes use of the following (compression) mechanisms for file archiving:
 - `.tar`
 - `.tar.gz`
 - `.zip`


For each of these mechanisms a version exist. For the `.tar` and `.tar.gz` 
versions, two additional versions exists with similar contents, but different
entries in their file tables. The regular version contains an entry for 
`metadata.json` while the `*.dot.tar` and `*.dot.tar.gz` versions contain 
entries for `./metadata.json` in their file tables. These additional versions
were created as a result of the observation that both file table structures
exist in different `.box` files.