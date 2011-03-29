package com.duosecurity;

public final class DuoIFRAME {
	private static final String REQUEST_PREFIX = "TX";
	private static final int REQUEST_EXPIRE = 300;
	private static final String RESPONSE_PREFIX = "AUTH";

	public static String signRequest(String skey, String ikey, String username) {
		long ts = System.currentTimeMillis() / 1000;
		long expire_ts = ts + REQUEST_EXPIRE;
		String expire = Long.toString(expire_ts);

		String val = username + "|" + ikey + "|" + expire;
		String cookie = REQUEST_PREFIX + "|" + Base64.encodeBytes(val.getBytes());

		String sig;
		try {
			sig = Util.hmacSign(skey, cookie);
		} catch (Exception e) {
			return null;
		}

		return cookie + "|" + sig;
	}

	public static String verifyResponse(String skey, String sig_response)
	{
		try {
			long ts = System.currentTimeMillis() / 1000;

			String[] parts = sig_response.split("\\|");
			if (parts.length != 3) {
				return null;
			}

			String u_prefix = parts[0];
			String u_b64 = parts[1];
			String u_sig = parts[2];

			String sig = Util.hmacSign(skey, u_prefix + "|" + u_b64);
			if (!Util.hmacSign(skey, sig).equals(Util.hmacSign(skey, u_sig))) {
				return null;
			}

			if (!u_prefix.equals(RESPONSE_PREFIX)) {
				return null;
			}

			byte[] decoded = Base64.decode(u_b64);
			String val = new String(decoded);
			
			String[] cookie_parts = val.split("\\|");
			if (cookie_parts.length != 3) {
				return null;
			}

			String username = cookie_parts[0];
			String expire = cookie_parts[2];

			long expire_ts = Long.parseLong(expire);
			if (ts >= expire_ts) {
				return null;
			}

			return username;
		} catch (Exception e) {
			return null;
		}
	}
}