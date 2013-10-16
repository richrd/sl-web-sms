sl-web-sms
==========

Python lib for sending free SMS-messages via oma.saunalahti.fi web interface.

_Usage:_

import sl_web_sms

service = sl_web_sms.SaunalahtiWebSMS()
service.Login(user,pw)
service.Send(from,to,message)
