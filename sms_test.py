 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test.py: Tests sl_web_sms lib for sending sms messages."""

__author__      = "Richard Lewis"
__copyright__   = "Copyright 2013, Richard Lewis"
__license__     = "MIT"
__version__     = "0.1"




import sl_web_sms



def QueryPassword():
    try:
        import getpass
        p = getpass.getpass()
    except:
        print "Warning, password input will be shown."
        p = raw_input("Password: ")
    return p


def RunTest():
    # try:
    #     credentials = raw_input("Username: "),QueryPassword()
    # except:
    #     print ""
    #     print "Login canceled."
    #     return False

    credentials=("0445310791","a8uahiry")

    service = sl_web_sms.SaunalahtiWebSMS()
    if not service.Login(credentials[0],credentials[1]):
        print "Login failed, check username and password."
        return False

    print "Logged in!"
    testmsg = "Hello world! äö!\"#¤%&/()=?+´^Å*-_.,:;|<>@£$‰{[]}\\"
    # testmsg = "Hello world!"
    if not service.Send(credentials[0],testmsg):
        print "Failed to send message!";
        return False
    print "Sent char test to your number."



RunTest()