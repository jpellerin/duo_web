from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urlparse
import ConfigParser
import cgi

import cookie
import duo_web


class RequestHandler(SimpleHTTPRequestHandler, cookie.RequestHandler):

    def error(self, msg):
        """
        Write an error 400.
        """
        self.send_response(400, msg)
        self.end_headers()
        self.wfile.write(msg)            

    def serve_file(self):
        """
        If a file exists corresponding to the request's path, serve it.
        Otherwise, raise IOError.
        """
        path = self.translate_path(self.path)
        try:
            f = open(path, 'rb')
        except IOError:
            raise
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def require_query(self, name):
        """
        Return the query argument value for given argument name,
        or raise ValueError.
        """
        path = urlparse.urlparse(self.path)
        try:
            return urlparse.parse_qs(path.query)[name][0]
        except:
            raise ValueError

    def require_post(self, name):
        """
        Return the POST argument value for given argument name,
        or raise ValueError.
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],})
        try:
            return form[name].value
        except:
            raise ValueError
                               
    def do_GET(self):
        try:
            self.serve_file()
        except IOError:
            pass
        else:
            return                      # we served a file from the FS

        # Get the username from the 'user' query argument.  In real life,
        # this will usually be done with framework-appropriate authentication.
        # The local username will be used as the Duo username as well.
        try:
            username = self.require_query('user')
        except ValueError:
            self.error('user query parameter is required')
            return
        self.send_response(200)
        # Set a cookie to compare with the Duo return
        self.set_secure_cookie('user', username)
                
        self.end_headers()

        sig_request = duo_web.sign_request(skey, ikey, username)
        self.wfile.write(
            "<script src='/Duo-Web-v1.bundled.min.js'></script>"
            "<script>"
            "Duo.init({'host':'%(host)s', 'sig_request':'%(sig_request)s'});"
            "</script>"
            "<iframe height='100%%' width='100%%' id='duo_iframe' />"
            % {'host':host, 'sig_request':sig_request})
        return

    def do_POST(self):
        try:
            sig_response = self.require_post('sig_response')
        except ValueError:
            self.error('sig_response post parameter is required')
            return
        user = duo_web.verify_response(skey, sig_response)
        if user is None:
            self.wfile.write('Did not authenticate with Duo.')
        elif self.get_secure_cookie('user') != user:
            self.wfile.write('Duo user does not match local user.')
        else:
            self.wfile.write('Authenticated with Duo as %s.' % user)
        
                                                
if __name__ == '__main__':
    global ikey, skey, host
    config = ConfigParser.ConfigParser()
    config.read('duo.conf')
    config_d = dict(config.items('duo'))
    ikey = config_d['ikey']
    skey = config_d['skey']
    host = config_d['host']        
    config_d = dict(config.items('app'))
    cookie_secret = config_d['cookie_secret']

    server = HTTPServer(('', 8080), RequestHandler)
    server.cookie_secret = cookie_secret
    server.serve_forever()
