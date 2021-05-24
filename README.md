# exceptionalpy
## features
- Handler
  - [X] handle exceptions
    - [X] print stacktrace
    - [X] forward stacktrace to notifier

- BaseNotifier
  - [X] provide interface for extensions
  
- HTTPNotifier
  - [X] send stacktrace via POST to specified url
  
- SMTPNotifier
  - [X] send stacktrace via Mail to specified email addresses

- Rescuer
  - [ ] Manager like interface for threads / processes
  - [ ] Capture exceptions, 
  
## usage
```python
from exceptionalpy import ex, exceptionalpy_handler as handler

# lets be verbose
handler.verbose = True
# you can either just catch all exceptions with
handler.init()
# and then stop again with
handler.deinit()

# or you can decorate the functions of which you want the exceptions to be caught
@ex()
def i_will_throw():
    raise BaseException


# before any exceptions happen, you can also attach a notifier
from exceptionalpy.HTTP import HTTPNotifier
handler.notifier = HTTPNotifier("https://my-server:1337/api/exceptional", "POST")

# or just use a completely different handler
from exceptionalpy.SMTP import SMTPSHandler
handler = SMTPSHandler(("127.0.0.1", 25), # which SMTP server to use
                       "exceptionalpy@locahost", # the sender address
                       "dev@localhost", # the receiver address
                       "There was an exception in your program") # the subject
#  nothing bad will happen if you don't call
handler.deinit()
# beforehand. you can do it, but it's a waste of cpu cycles.

i_will_throw()
print("I will still be printed")
```