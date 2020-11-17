# parser_helpers
Helper Utils to View and Compare Docstrings Between Argument Parsers and API Methods

Disclaimer : there probably exists a better method of doing this, but ATM it's easier for
me to just go with this hack

The mdciao has CLI scripts that wrap around API methods. The CLI docstrings and the API docstrings
track the same arguments but in annoyingly different ways...there's a lot of shared boilerplate
but also some slight differences in typing (strs vs other objects) and return values

This module basically iterates through the CLI-script parsers, fuzzy-matches their name to API methods
and presents the docstring side by side for equivalent args or kwargs, making copy-pasting easier.
