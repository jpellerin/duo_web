package com.duosecurity;

import junit.framework.TestCase;

public class DuoTest extends TestCase {

	/* Dummy IKEY and SKEY values */
	private static final String IKEY = "DIXXXXXXXXXXXXXXXXXX";
	private static final String SKEY = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef";

	/* Dummy username */
	private static final String USER = "testuser";

	/* Dummy response signatures */
	private static final String INVALID_RESPONSE = "AUTH|INVALID|SIG";
	private static final String EXPIRED_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTMwMDE1Nzg3NA==|cb8f4d60ec7c261394cd5ee5a17e46ca7440d702";
	private static final String FUTURE_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTYxNTcyNzI0Mw==|d20ad0d1e62d84b00a3e74ec201a5917e77b6aef";

	public void testSignRequest() {
		String request_sig = DuoIFRAME.signRequest(SKEY, IKEY, USER);
		assertNotNull(request_sig);
	}

	public void testVerifyResponse() {
		String invalid_user = DuoIFRAME.verifyResponse(SKEY, INVALID_RESPONSE);
		assertNull(invalid_user);

		String expired_user = DuoIFRAME.verifyResponse(SKEY, EXPIRED_RESPONSE);
		assertNull(expired_user);

		String future_user = DuoIFRAME.verifyResponse(SKEY, FUTURE_RESPONSE);
		assertNotNull(future_user);
		assertTrue(future_user.equals(USER));
	}
}
