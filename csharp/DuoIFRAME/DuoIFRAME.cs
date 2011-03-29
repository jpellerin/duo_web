/*
 * DuoIFRAME.cs
 *
 * Copyright (c) 2011 Duo Security
 * All rights reserved, all wrongs reversed.
 */

using System;
using System.IO;
using System.Net;
using System.Web;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Security.Cryptography;

namespace Duo
{
	public static class IFRAME
	{
		const string REQUEST_PREFIX = "TX";
		const int REQUEST_EXPIRE = 300;
		const string RESPONSE_PREFIX = "AUTH";

		/// <summary>
		/// Generate a signed request for the Duo IFRAME.
		/// The returned sig_request should be passed into the Duo.init() call
		/// in the rendered web page used for secondary authentication.
		/// </summary>
		/// <param name="skey">Duo secret key</param>
		/// <param name="ikey">Duo integration key</param>
		/// <param name="username">Primary-authenticated username</param>
		/// <returns>signed request</returns>
		public static string SignRequest(string skey, string ikey, string username)
		{
			int ts = (int) (DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;
			int expire_ts = ts + REQUEST_EXPIRE;
			string expire = expire_ts.ToString();

			string val = username + "|" + ikey + "|" + expire;
			string cookie = REQUEST_PREFIX + "|" + Encode64(val);

			string sig = HmacSign(skey, cookie);

			return cookie + "|" + sig;
		}

		/// <summary>
		/// Validate the signed response returned from the Duo IFRAME.
		/// Returns the username of the successfully-authenticated user 
		/// (which should be verified against the original username passed 
		/// to SignRequest()), or null.
		/// </summary>
		/// <param name="skey">Duo secret key</param>
		/// <param name="sig_response">The signed response POST'ed to the server</param>
		/// <returns>The username of the authenticated user, or null</returns>
		public static string VerifyResponse(string skey, string sig_response)
		{
			try {
				int ts = (int) (DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;

				string[] parts = sig_response.Split('|');
				if (parts.Length != 3) {
					return null;
				}

				string u_prefix = parts[0];
				string u_b64 = parts[1];
				string u_sig = parts[2];

				string sig = HmacSign(skey, u_prefix + "|" + u_b64);
				if (HmacSign(skey, sig) != HmacSign(skey, u_sig)) {
					return null;
				}

				if (u_prefix != RESPONSE_PREFIX) {
					return null;
				}

				string val = Decode64(u_b64);
				string[] cookie_parts = val.Split('|');
				if (cookie_parts.Length != 3) {
					return null;
				}

				string username = cookie_parts[0];
				string ikey = cookie_parts[1];
				string expire = cookie_parts[2];

				int expire_ts = Convert.ToInt32(expire);
				if (ts >= expire_ts) {
					return null;
				}
				
				return username;
			} catch {
				return null;
			}
		}

		private static string HmacSign(string skey, string data)
		{
			byte[] key_bytes = ASCIIEncoding.ASCII.GetBytes(skey);
			HMACSHA1 hmac = new HMACSHA1(key_bytes);

			byte[] data_bytes = ASCIIEncoding.ASCII.GetBytes(data);
			hmac.ComputeHash(data_bytes);

			string hex = BitConverter.ToString(hmac.Hash);
			return hex.Replace("-", "").ToLower();
		}

		private static string Encode64(string plaintext)
		{
			byte[] plaintext_bytes = ASCIIEncoding.ASCII.GetBytes(plaintext);
			string encoded = System.Convert.ToBase64String(plaintext_bytes);
			return encoded;
		}

		private static string Decode64(string encoded)
		{
			byte[] plaintext_bytes = System.Convert.FromBase64String(encoded);
			string plaintext = ASCIIEncoding.ASCII.GetString(plaintext_bytes);
			return plaintext;
		}
	}
}
