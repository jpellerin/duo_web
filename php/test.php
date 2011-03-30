<?php

require_once("duo_web.php");

const IKEY = "DIXXXXXXXXXXXXXXXXXX";
const SKEY = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef";

const USER = "testuser";

const INVALID_RESPONSE = "AUTH|INVALID|SIG";
const EXPIRED_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTMwMDE1Nzg3NA==|cb8f4d60ec7c261394cd5ee5a17e46ca7440d702";
const FUTURE_RESPONSE = "AUTH|dGVzdHVzZXJ8RElYWFhYWFhYWFhYWFhYWFhYWFh8MTYxNTcyNzI0Mw==|d20ad0d1e62d84b00a3e74ec201a5917e77b6aef";

echo "Generating a signed request...\n";
$request_sig = Duo::signRequest(SKEY, IKEY, USER);
echo "Generated request_sig: " . $request_sig . "\n";

echo "-------------------------------------------------\n";

echo "Validating invalid signed response...\n";
$invalid_user = Duo::verifyResponse(SKEY, INVALID_RESPONSE);
if ($invalid_user == NULL) {
    echo "Got expected result: returned user is null\n";
} else {
    echo "Got unexpected result: returned user is not null\n";
}

echo "Validating expired signed response...\n";
$expired_user = Duo::verifyResponse(SKEY, EXPIRED_RESPONSE);
if ($expired_user == NULL) {
    echo "Got expected result: returned user is null\n";
} else {
    echo "Got unexpected result: returned user is not null\n";
}

echo "Validating future signed response...\n";
$future_user = Duo::verifyResponse(SKEY, FUTURE_RESPONSE);
if ($future_user == USER) {
    echo "Got expected result: returned user is " . $future_user . "\n";
} else {
    echo "Got unexpected result: returned user is not " . $future_user . "\n";
}

?>
