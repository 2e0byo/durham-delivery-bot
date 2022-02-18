# A bot to bulk reserve delivery of items from Durham University Library

Durham university has a few libraries.  It also has a system to get books from
satellite libraries into the main library.  It also has a basic 'book cart'
where you can save records you find whilst browsing the catalogue.
Unfortunately it has no way of plugging these together: the only way to get from
a bunch of books in the cart to a bunch of deliveries is to click on each record
manually, log in (again, this time http basic auth), fill in a form, and press submit.

In this repo you will find a bot which automates this process.

## Installation

Clone/download this repo, and then run:

```bash
poetry install
poetry shell
```

if you want to install system-wide, use `poetry build` and then use pip to
install the wheel inside `dist`

## Usage

- Browse the catalogue and add books to the cart
- Go to the book cart, select "Screen" as the export target on top, and press submit.
- Save the resulting html page somewhere.
- run `durham-delivery-bot requests /path/to/saved/page.html`


## Saving the current page with qutebrowser

`qutebrowser` has no 'save current page' option.  There is `:donwload`, but that
issues a get request for the current url, which is no good here.  Fortunately
the workaround is easy (and obvious once you think of it): open the devtools,
switch to "elements", right-click the outmost element (the html document), copy,
and paste into a file.

## Explanation

The exported page is scraped with beautifulsoup to extract the record
permalinks.  The browser logs in, and then visits the links one by one.  Since
the website relies on inline javascript to open each link in a new tab (sic!)
which is tedious, we extract the link target.  We then take only the record from
that url target, construct a *new* url injecting credentials in the url (BAD
BAD! but chromedriver uses a new profile each time...), and then fill in the form.

## FAQ

- **Isn't one of the steps above redundant?  You already have the bib number!**
  Yeah, I just thought of that too.  That's what rapid development is about,
  right?  I don't want to reserve any more books, though, so I can't test it...
  Can you tell I wrote this in a hurry?
