# 
# duo_iframe.py
#
# Copyright (c) 2011 Duo Security
# All rights reserved, all wrongs reversed.

import base64
import hashlib
import hmac
import time

REQUEST_PREFIX = 'TX'
REQUEST_EXPIRE = 300
RESPONSE_PREFIX = 'AUTH'

def _hmac_sha1(key, msg):
    ctx = hmac.new(key, msg, hashlib.sha1)
    return ctx.hexdigest()

def sign_request(skey, ikey, username):
    """Generate a signed request for the Duo IFRAME.
    The returned sig_request should be passed into the Duo.init()
    call in the rendered web page used for secondary authentication.
    
    Arguments:
    
    skey      -- Duo secret key
    ikey      -- Duo integration key
    username  -- Primary-authenticated username
    """
    exp = str(int(time.time()) + REQUEST_EXPIRE)

    val = '|'.join([ username, ikey, exp ])
    b64 = base64.b64encode(val)
    cookie = '%s|%s' % (REQUEST_PREFIX, b64)

    sig = _hmac_sha1(skey, cookie)

    return '%s|%s' % (cookie, sig)

def verify_response(skey, sig_response):
    """Validate the signed response returned from the Duo IFRAME.
    Returns the username of the successfully-authenticated user 
    (which should be verified against the original username passed 
    to sign_request()), or None.
    
    Arguments:
    
    skey          -- Duo secret key
    sig_response  -- The signed response POST'ed to the server
    """
    try:
        ts = int(time.time())
        u_prefix, u_b64, u_sig = sig_response.split('|')
        
        sig = _hmac_sha1(skey, '%s|%s' % (u_prefix, u_b64))
        if _hmac_sha1(skey, sig) != _hmac_sha1(skey, u_sig):
            return None

        if u_prefix != RESPONSE_PREFIX:
            return None

        user, ikey, exp = base64.b64decode(u_b64).split('|')

        if ts >= int(exp):
            return None

        return user
    except:
        pass
    return None
