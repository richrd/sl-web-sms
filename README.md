sl-web-sms
==========

Simple Python lib for sending free SMS-messages via oma.saunalahti.fi web interface.

### Usage ###
    import sl_web_sms

    # Methods 'Login' and 'Send' return True on success, otherwise False.
    # At the moment, no error handling is implemented, so use try & except.
    service = sl_web_sms.SaunalahtiWebSMS()
    try:
        service.Login(user,pw)

        message = u"Hello world!" # message data must be unicode

        # Automatically select which number to send from
        service.Send(to,message)

        # or

        # Select the first available number to send from
        service.Send(to,message,from=service.sender_numbers[0]) 

        print "Message sent."
    except Exception,e:
        print "Sorry, something broke:",e
