import time
import functools
import numpy as np

# time a function
def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print('total execution time',np.round(t1-t0,3),'seconds')
        return result
    return wrapper
    
import functools
import os
from datetime import datetime

# decorator for convinent time-based logging
def log_it(**log_info):
    def log_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # set destination and message for log
            log_name = 'test.txt'
            if 'log_name' in log_info:
                log_name = log_info['log_name']
                
            log_message = func.__name__
            if 'log_message' in log_info:
                log_message = log_info['log_message']
                
            # refresh log?
            refresh = False
            if 'refresh' in log_info:
                refresh = log_info['refresh']
                
            if refresh == True:
                if os.path.exists(log_name):
                    os.remove(log_name)
            
            dateTimeObj = datetime.now().replace(microsecond=0)
            print(dateTimeObj,'START:',log_message,file=open(log_name, "a"))
            try:
                result = func(*args, **kwargs)
                dateTimeObj = datetime.now().replace(microsecond=0)
                print(dateTimeObj,'SUCCESS:',log_message,file=open(log_name, "a"))   
            except:
                result = 0
                dateTimeObj = datetime.now().replace(microsecond=0)
                print(dateTimeObj,'FAILURE:',log_message,file=open(log_name, "a"))    
            return result
        return wrapper
    return log_decorator
    
    
import smtplib, ssl
import functools
import os

def email_decorator(func):
    # setup email sender
    sender_email = "your@email.com" 
    receiver_email = "your@email.com" 
    password = 'your_password'

    # email sender - just define the message
    def send_email(message):
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message
            )

    # wrap input function    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        email_message = func.__name__

        try: # sucess
            # run function
            result = func(*args, **kwargs)

            # compose message to send
            message = 'Subject: SUCCESS: function "' + email_message    + '" completed!'
            message += '\n\n'
            message += 'SUCCESS: function "' + email_message    + '" completed!'
            send_email(message)
        except:
            # compose message to send
            message = 'Subject: FAILED: function "' + email_message    + '" failed!'
            message += '\n\n'         
            message = 'FAILED: function "' + email_message    + '" failed!'
            send_email(message)
    return wrapper
