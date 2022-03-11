# A bot to bulk reserve delivery of items from Durham University Library

Durham university has a few libraries.  It also has a system to get books from
satellite libraries into the main library.  It also has a basic 'book cart'
where you can save records you find whilst browsing the catalogue.
Unfortunately it has no way of plugging these together: the only way to get from
a bunch of books in the cart to a bunch of deliveries is to click on each record
manually, log in (again, this time http basic auth), fill in a form, and press submit.

In this repo you will find a bot which automates this process.

It also prints a nicely formatted list of books to collect from each library,
sorted by shelfmark.

## Installation

Clone/download this repo, and then run:

```bash
poetry install
poetry shell
```

if you want to install system-wide, use `poetry build` and then use pip to
install the wheel inside `dist`.  Or run `make install`, which does exactly the
same thing.

## Usage

- Browse the catalogue and add books to the cart
- Go to the book cart, select "Screen" as the export target on top, and press submit.
- Save the resulting html page somewhere.
- run `durham-delivery-bot /path/to/saved/page.html`
- see `durham-delivery-bot --help` for more details.

**Warning:** the bot will attempt to request delivery from every library not
explicitly set as a source for collection in person.  This may or may not work;
you are advised to check.  You can use the `--dry-run` option to check what it
would try to reserve.


## Saving the current page with qutebrowser

`qutebrowser` has no 'save current page' option.  There is `:donwload`, but that
issues a get request for the current url, which is no good here.  Fortunately
the workaround is easy (and obvious once you think of it): open the devtools,
switch to "elements", right-click the outmost element (the html document), copy,
and paste into a file.

## Explanation

The exported page is scraped with beautifulsoup to extract the record
permalinks.  From this permalink we get the bib id; from that we build the
reserve/request delivery link.  We inject credentials in this url since Durham
currently uses plain authentication (over ssl) for the form
(BAD
BAD! but chromedriver uses a new profile each time...), and then fill in the form.

Note that at present the output provided by durham is broken in quite a lot of
ways, including commenting out the div for the first entry in the bib list. We
work around that.

