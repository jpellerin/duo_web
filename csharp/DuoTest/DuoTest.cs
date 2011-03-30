/*
 * DuoTest.cs
 *
 * Copyright (c) 2011 Duo Security
 * All rights reserved, all wrongs reversed.
 *
 * Simple test exercising the Duo Web SDK
 */

using System;
using System.Collections;
using System.Linq;
using System.Text;

using Duo;

namespace DuoTest
{
	class DuoTest
	{
		/* Dummy IKEY and SKEY values */
		const string IKEY = "DIXXXXXXXXXXXXXXXXXX";
		const string SKEY = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef";

		/* Dummy username */
		const string USER = "testuser";

		/* Dummy response signatures */
		const string INVALID_RESPONSE = "AUTH|INVALID|SIG";
		const string EXPIRED_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTMwMDE1Nzg3NA==|cb8f4d60ec7c261394cd5ee5a17e46ca7440d702";
		const string FUTURE_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTYxNTcyNzI0Mw==|d20ad0d1e62d84b00a3e74ec201a5917e77b6aef";

		static void Main(string[] args)
		{
			Console.WriteLine("Generating a signed request...");
			string request_sig = Duo.Web.SignRequest(SKEY, IKEY, USER);
			Console.WriteLine("Generated request_sig: " + request_sig);

			Console.WriteLine("-------------------------------------------------");

			Console.WriteLine("Validating invalid signed response...");
			string invalid_user = Duo.Web.VerifyResponse(SKEY, INVALID_RESPONSE);
			if (invalid_user == null) {
				Console.WriteLine("Got expected result: returned user is null");
			} else {
				Console.WriteLine("Got unexpected result: returned user is not null");
			}

			Console.WriteLine("Validating expired signed response...");
			string expired_user = Duo.Web.VerifyResponse(SKEY, EXPIRED_RESPONSE);
			if (expired_user == null) {
				Console.WriteLine("Got expected result: returned user is null");
			} else {
				Console.WriteLine("Got unexpected result: returned user is not null");
			}

			Console.WriteLine("Validating future signed response...");
			string future_user = Duo.Web.VerifyResponse(SKEY, FUTURE_RESPONSE);
			if (future_user == USER) {
				Console.WriteLine("Got expected result: returned user is " + future_user);
			} else {
				Console.WriteLine("Got unexpected result: returned user is not " + future_user);
			}
		}
	}
}
