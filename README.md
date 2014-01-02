ffgrep
======

ffgrep - A grep-like command line tool (written in Python) to search text files in a given directory and (optionally)
open a text editor to the matching line. I wrote this tool to primarily to help navigate large code bases and make quick
changes.

Status
======
Code is currently under development and not available for use yet.

Installation and Pre-Requisites
===============================
Requires Python 2.7 or higher. Should be compatible with Python 3.x, but testing is needed to verify that there are no
Python 3 specific issues.

Basic Usage
===========

Search for `"Search term"` in the directory `/path/to/search`:

```bash
python ffgrep.py "Search term" /path/to/search
```

Perform a case-insensitive search for `"SEARCH TERM"` in path `/path/to/search` and files `/path2/file1.txt` and
`/path2/file2.txt`:

```bash
python ffgrep.py -i "SEARCH TERM" /path/to/search /path2/file1.txt /path2/file2.txt
```

Command Line Options
====================

```bash
ffgrep.py [-h] [-i] S [paths ...]
```

Required:
S                   The search term that you are attempting to match

Optional:
paths               One or more files or paths that should be searched (default: current directory)
-h, --help          Show help information regarding command line options
-i, --ignore-case   Ignore case when searching for the specified term

License
=======
MIT-licensed - Use or adapt the source code for any purpose. Software is provided "as is" with no warranty.
Full licensing details are included in the [LICENSE](LICENSE) file.
