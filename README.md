# Overview

**duo_web** - Duo two-factor authentication for web applications

Duo provides simple two-factor authentication as a service via:

1.  Phone callback
2.  SMS-delivered one-time passcodes
3.  Duo mobile app to generate one-time passcodes
4.  Duo mobile app for smartphone push authentication
5.  Duo hardware token to generate one-time passcodes

This package allows a web developer to quickly add Duo's interactive, self-service, two-factor authentication to any web login form — without setting up secondary user accounts directory synchronization, servers, or hardware.

What's here:

* `js` - Duo Javascript library, to be hosted by your webserver.
* `csharp`, `java`, `php`, `python` - Duo web SDKs for ASP.NET, Java, PHP, and Python environments. See the README and examples contained within for details.
* `demos` -  Example integrations demonstrating how to use the duo_web SDK.

# Usage

How it works:

1. The original server-side login form handler is modified to return a secondary login page on success, with a few lines of Duo's Javascript snippet and IFRAME.
2. The user interacts with the Duo IFRAME for secondary login (or to enroll themselves if it's their first Duo login)
3. Duo's Javascript posts the secure result token from the IFRAME to a secondary login handler which verifies the token and sets auth state (as the original login form handler did, likely in a cookie/session).

Eval users (e-mail duo_web@duosecurity.com to request a trial): be sure to set your Duo API host to `api-eval.duosecurity.com`.

# Support

Questions? Join the duo_web mailing list at
http://groups.google.com/group/duo_web

Report any bugs, feature requests, etc. to us directly:
https://github.com/duosecurity/duo_web/issues

Have fun!

http://duosecurity.com
