
## Saving the current page with qutebrowser

Qutebrowser has no 'save current page' option.  There is `:donwload`, but that
issues a get request for the current url, which is no good here.  Fortunately
the workaround is easy (and obvious once you think of it): open the devtools,
switch to "elements", right-click the outmost element (the html document), copy,
and paste into a file.
