# bookfinder-multisearch
A *very* quickly hacked together tool to search bookfinder.com for a whole file
worth of books rather than just one at a time. Why? Because this semester I have
a ridiculous number of books to buy and copy-pasting gets boring.

Update for 2017: As it turns out, I have a ridiculous number of books to buy
*every* semester.

# Installation
bookfinder-multisearch is written in Python 2.7. It requires:
* Python 2.7.9 or greater
* Requests
* lxml
* argparse
* Possibly some assembly; your mileage may vary.

# Usage
Lay out your list like this:
```
Book Title One: No Author, Just The Title
Book Title Two: Yeah, Just The Title
Book Title Three: I Told You This Was Quickly Hacked Together
etc.
```

Then, run:

> python bookfinder.py <path_to_book_file>

Voila. Every once-in-a-while the script will fail because bookfinder.com did
something funky. Try re-running the script before pronouncing it broken.

(If re-running the script AND double-checking your version of python doesn't
fix your problem, submit an issue!)
