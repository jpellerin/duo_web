Demonstration of a simple Python web server with Duo authentication.

Tested with Python 2.6.

# Install/Run

To set up, edit duo.conf with the appropriate `ikey`, `skey`, `host`,
and `cookie_secret` values.  `cookie_secret` should be a random string.

To run the server on port 8080:

    python server.py

# Usage

Visit the root URL with a 'user' argument, e.g.
'http://localhost:8080/user=myname'.



