sl-web-sms
==========

Simple Python lib for sending free SMS-messages via oma.saunalahti.fi web interface.

### Usage ###
    import sl_web_sms

    # methods 'Login' and 'Send' return True on success, otherwise False.
    # at the moment, no error handling is implemented, so use try & except
    service = sl_web_sms.SaunalahtiWebSMS()
    try:
        service.Login(user,pw)
        service.Send(from,to,message)
        print "Message sent."
    except Exception,e:
        print "Sorry, something broke:",e
