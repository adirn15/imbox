import unittest
from imbox.parser import *

import sys
if sys.version_info.minor < 3:
    SMTP = False
else:
    from email.policy import SMTP


raw_email = """Delivered-To: johndoe@gmail.com
X-Originating-Email: [martin@amon.cx]
Message-ID: <test0@example.com>
Return-Path: martin@amon.cx
Date: Tue, 30 Jul 2013 15:56:29 +0300
From: Martin Rusev <martin@amon.cx>
MIME-Version: 1.0
To: John Doe <johndoe@gmail.com>
Subject: Test email - no attachment
Content-Type: multipart/alternative;
    boundary="------------080505090108000500080106"
X-OriginalArrivalTime: 30 Jul 2013 12:56:43.0604 (UTC) FILETIME=[3DD52140:01CE8D24]

--------------080505090108000500080106
Content-Type: text/plain; charset="ISO-8859-1"; format=flowed
Content-Transfer-Encoding: 7bit

Hi, this is a test email with no attachments

--------------080505090108000500080106
Content-Type: text/html; charset="ISO-8859-1"
Content-Transfer-Encoding: 7bit

<html><head>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body
 bgcolor="#FFFFFF" text="#000000">
Hi, this is a test email with no <span style="font-weight: bold;">attachments</span><br>
</body>
</html>

--------------080505090108000500080106--
"""

raw_email_encoded = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
Date: Sat, 26 Mar 2016 13:55:30 +0300 (FET)
From: sender@example.com
To: receiver@example.com
Message-ID: <811170233.1296.1345983710614.JavaMail.bris@BRIS-AS-NEW.site>
Subject: =?ISO-8859-5?B?suvf2OHa0CDf3iDa0ODi1Q==?=
MIME-Version: 1.0
Content-Type: multipart/mixed; 
	boundary="----=_Part_1295_1644105626.1458989730614"

------=_Part_1295_1644105626.1458989730614
Content-Type: text/html; charset=ISO-8859-5
Content-Transfer-Encoding: quoted-printable

=B2=EB=DF=D8=E1=DA=D0 =DF=DE =DA=D0=E0=E2=D5 1234
------=_Part_1295_1644105626.1458989730614--
"""

raw_email_encoded_needs_refolding = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
Date: Sat, 26 Mar 2016 13:55:30 +0300 (FET)
From: sender@example.com
To: "Receiver" <receiver@example.com>, "Second\r\n Receiver" <recipient@example.com>
Message-ID: <811170233.1296.1345983710614.JavaMail.bris@BRIS-AS-NEW.site>
Subject: =?ISO-8859-5?B?suvf2OHa0CDf3iDa0ODi1Q==?=
MIME-Version: 1.0
Content-Type: multipart/mixed; 
    boundary="----=_Part_1295_1644105626.1458989730614"

------=_Part_1295_1644105626.1458989730614
Content-Type: text/html; charset=ISO-8859-5
Content-Transfer-Encoding: quoted-printable

=B2=EB=DF=D8=E1=DA=D0 =DF=DE =DA=D0=E0=E2=D5 1234
------=_Part_1295_1644105626.1458989730614--
"""


raw_email_encoded_bad_multipart = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
From: sender@example.com
To: "Receiver" <receiver@example.com>, "Second\r\n Receiver" <recipient@example.com>
Subject: Re: Looking to connect with you...
Date: Thu, 20 Apr 2017 15:32:52 +0000
Message-ID: <BN6PR16MB179579288933D60C4016D078C31B0@BN6PR16MB1795.namprd16.prod.outlook.com>
Content-Type: multipart/related;
	boundary="_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_";
	type="multipart/alternative"
MIME-Version: 1.0
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: multipart/alternative;
	boundary="_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_"
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64
SGkgRGFuaWVsbGUsDQoNCg0KSSBhY3R1YWxseSBhbSBoYXBweSBpbiBteSBjdXJyZW50IHJvbGUs
Y3J1aXRlciB8IENoYXJsb3R0ZSwgTkMNClNlbnQgdmlhIEhhcHBpZQ0KDQoNCg==
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: base64
PGh0bWw+DQo8aGVhZD4NCjxtZXRhIGh0dHAtZXF1aXY9IkNvbnRlbnQtVHlwZSIgY29udGVudD0i
CjwvZGl2Pg0KPC9kaXY+DQo8L2JvZHk+DQo8L2h0bWw+DQo=
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_--
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: image/png; name="=?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?="
Content-Description: =?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?=
Content-Disposition: inline;
	filename="=?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?="; size=488;
	creation-date="Thu, 20 Apr 2017 15:32:52 GMT";
	modification-date="Thu, 20 Apr 2017 15:32:52 GMT"
Content-ID: <254962e2-f05c-40d1-aa11-0d34671b056c>
Content-Transfer-Encoding: base64
iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ
cvED9AIR3TCAAAMAqh+p+YMVeBQAAAAASUVORK5CYII=
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_--
"""


class TestParser(unittest.TestCase):

    def test_parse_email(self):
        parsed_email = parse_email(raw_email)

        self.assertEqual(raw_email, parsed_email.raw_email)
        self.assertEqual('Test email - no attachment', parsed_email.subject)
        self.assertEqual('Tue, 30 Jul 2013 15:56:29 +0300', parsed_email.date)
        self.assertEqual('<test0@example.com>', parsed_email.message_id)

    def test_parse_email_encoded(self):
        parsed_email = parse_email(raw_email_encoded)

        self.assertEqual('Выписка по карте', parsed_email.subject)
        self.assertEqual('Выписка по карте 1234', parsed_email.body['html'][0])

    def test_parse_email_bad_multipart(self):
        parsed_email = parse_email(raw_email_encoded_bad_multipart)
        self.assertEqual("Re: Looking to connect with you...", parsed_email.subject)

    def test_parse_email_ignores_header_casing(self):
        self.assertEqual('one', parse_email('Message-ID: one').message_id)
        self.assertEqual('one', parse_email('Message-Id: one').message_id)
        self.assertEqual('one', parse_email('Message-id: one').message_id)
        self.assertEqual('one', parse_email('message-id: one').message_id)

    # TODO - Complete the test suite
    def test_parse_attachment(self):
        pass

    def test_decode_mail_header(self):
        pass

    def test_get_mail_addresses(self):

        to_message_object = email.message_from_string("To: John Doe <johndoe@gmail.com>")
        self.assertEqual([{'email': 'johndoe@gmail.com', 'name': 'John Doe'}], get_mail_addresses(to_message_object, 'to'))

        from_message_object = email.message_from_string("From: John Smith <johnsmith@gmail.com>")
        self.assertEqual([{'email': 'johnsmith@gmail.com', 'name': 'John Smith'}], get_mail_addresses(from_message_object, 'from'))

    def test_parse_email_with_policy(self):
        if not SMTP:
            return

        message_object = email.message_from_bytes(
            raw_email_encoded_needs_refolding,
            policy=SMTP.clone(refold_source='all')
        )

        self.assertEqual([
            {'email': 'receiver@example.com', 'name': 'Receiver'},
            {'email': 'recipient@example.com', 'name': 'Second Receiver'}
        ], get_mail_addresses(message_object, 'to'))
