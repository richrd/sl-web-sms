#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""sl_web_sms.py: Sends sms messages via oma.saunalahti.fi web interface."""

__author__      = "Richard Lewis"
__copyright__   = "Copyright 2013, Richard Lewis"
__license__     = "MIT"
__version__     = "0.1"

import urllib,httplib,string


# Get an escaped version of a single character.
def get_char_encoded(c):
    return hex(ord(c)).replace("0x","%").upper()

# Custom escaping, escapes all except 'safe' characters.
def escape(s, safe = '/'):
    # FIXME: some special characters are incorectly escaped.
    always_safe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-'
    safe = always_safe + safe
    result = ""
    for ch in s:
        if ch not in safe:
            result = result + get_char_encoded(ch)
        else:
            result = result + ch
    return result

# Get a substring of a string based on two string delimi0ters
def get_string_between(start,stop,s):
    i1 = s.find(start)
    if i1 == -1: return False
    s = s[i1+len(start):]
    i2 = s.find(stop)
    if i2 == -1: return False
    s = s[:i2]
    return s


# Main class
class SaunalahtiWebSMS:
    def __init__(self):
        self.host = 'oma.saunalahti.fi'
        
        # Parameters used to pass the login data.
        self.login_username_field = 'username'
        self.login_password_field = 'password'
        
        self.default_headers = {"Content-type": "application/x-www-form-urlencoded",
                                       "Accept": "text/plain",
                                       "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20100101 Firefox/16.0",
                                        }

        self.sms_sender_field = 'sender'
        self.sms_recipients_field = 'recipients'
        self.sms_message_field = 'text'
        self.sms_length_field = 'size'
        self.sms_submit_field = 'send'
        
        self.login_path = '/settings/smsSend'
        self.login_method = 'POST'
        
        self.sender_numbers = None
        self.current_status = None
        
        self.AUTH_COOKIE = None


    #
    # Get the cookie necessary for authentication.
    #
    def _get_auth_cookie(self):
        conn = httplib.HTTPSConnection(self.host)
        conn.request('GET', self.login_path)
        response = conn.getresponse()
        chocolate_chip_cookie = response.getheader('set-cookie')
        return chocolate_chip_cookie # Omnom!

    #
    # Return list containing the numbers that can be used as the sender number. Values are str.
    #
    def _get_sender_numbers(self,data = None):
        if data == None:
            params = None

            headers=self.default_headers
            headers["Cookie"] = self.AUTH_COOKIE

            conn = httplib.HTTPSConnection(self.host)
            conn.request("POST", "/settings/smsSend", params, headers)
            data = conn.getresponse().read()
        part = get_string_between("<select name=\"sender\"","</select>",data)
        lines = string.split(part,"\n")
        numbers = []
        for line in lines:
            line = string.strip(line)
            if line.startswith("<option"):
                num = get_string_between("value=\"","\"",line)
                numbers.append(num)
        return numbers

    #
    # Return list of format [msgs sent, free msgs left, paid msgs left]. All values are int.
    #
    def _get_current_status(self,data = None):
        if data == None:
            params = None

            headers=self.default_headers
            headers["Cookie"] = self.AUTH_COOKIE

            conn = httplib.HTTPSConnection(self.host)
            conn.request("POST", "/settings/smsSend", params, headers)
            data = conn.getresponse().read()
        piece = get_string_between("hetken tilanne:</td>","</td>",data)
        lines = piece.split("\n")
        values=[]
        for line in lines:
            if line.find(":")!=-1:
                l = get_string_between(":","<",line).strip()
                l = int(l)
                values.append(l)
        return values

    #
    # Authenticate so that messages can be sent.
    #
    def _login(self,user,password):
        self.username = user
        self.password = password

        self.AUTH_COOKIE = self._get_auth_cookie()
        params = {self.login_username_field: self.username,
                    self.login_password_field: self.password
        }
        params = urllib.urlencode(params)

        headers=self.default_headers
        headers["Cookie"] = self.AUTH_COOKIE

        conn = httplib.HTTPSConnection(self.host)
        conn.request(self.login_method, self.login_path, params, headers)
        response = conn.getresponse()
        return response


    #
    # Send an sms message.
    #
    def _send_sms(self,sender,recipients,message):
        params = {self.sms_sender_field: sender,
                    self.sms_recipients_field: recipients,
                    self.sms_length_field: str(len(message)),
                    self.sms_submit_field: u"Laheta",
        }
        params = urllib.urlencode(params)
        params = params + "&"+self.sms_message_field+"=" + escape(message)

        headers=self.default_headers
        headers["Cookie"] = self.AUTH_COOKIE

        conn = httplib.HTTPSConnection(self.host)
        conn.request("POST", "/settings/smsSend", params, headers)
        response = conn.getresponse()
        return response


    def Login(self,user,password):
        response = self._login(user,password)
        
        success_str="form action=\"smsSend\""
        
        raw_data = response.read()
        if(raw_data.find(success_str) != -1):
            self.sender_numbers = self._get_sender_numbers(raw_data)
            self.current_status = self._get_current_status(raw_data)
            return True
        return False

    def Send(self,sender,recipients,message):
        response = self._send_sms(sender,recipients,message)
        raw_data = response.read().decode("ISO-8859-1")
        success_str=u"Viesti lähetetty."
        if(raw_data.find(success_str) != -1):
            return True
        return False

# Test sending a message.
def Test():
    service = SaunalahtiWebSMS()
    if not service.Login("user","pass"):
        print "Login failed, check username and password."
        print "You will need a Saunalahti customer account."
        return False

    print "Status [sent,free,paid]: ",service._get_current_status()
    print "Available 'from' numbers: ",service._get_sender_numbers()

    # From-number must be one of the numbers in list returned by _get_sender_numbers()
    if not service.Send("from","to","message"):
        print "Failed to send message! Check for invalid from/to value, or too long message."
        return False
    print "Message sent!"
    return True


    
if __name__ == "__main__":
    Test()
