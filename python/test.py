#!/usr/bin/env python

'''Simple tests for Duo Web SDK'''

import unittest
import duo_web

IKEY = "DIXXXXXXXXXXXXXXXXXX";
SKEY = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef";

USER = "testuser";

INVALID_RESPONSE = "AUTH|INVALID|SIG";
EXPIRED_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTMwMDE1Nzg3NA==|cb8f4d60ec7c261394cd5ee5a17e46ca7440d702";
FUTURE_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTYxNTcyNzI0Mw==|d20ad0d1e62d84b00a3e74ec201a5917e77b6aef";

class TestSDK(unittest.TestCase):

    def test_sign_request(self):
        request_sig = duo_web.sign_request(SKEY, IKEY, USER)
        self.assertNotEqual(request_sig, None)

    def test_verify_response(self):
        invalid_user = duo_web.verify_response(SKEY, INVALID_RESPONSE)
        self.assertEqual(invalid_user, None)

        expired_user = duo_web.verify_response(SKEY, EXPIRED_RESPONSE)
        self.assertEqual(expired_user, None)

        future_user = duo_web.verify_response(SKEY, FUTURE_RESPONSE)
        self.assertEqual(future_user, USER)

if __name__ == '__main__':
    unittest.main()
