# exceptionalpy
## install
```shell
pip3 install exceptionalpy
# or, assuming you have git installed
pip3 install git+https://github.com/nbdy/exceptionalpy
```

## features
- [X] exception handling decorator (ex / catch)
- [X] timing decorator (ti / timeit)
- [X] exception handling and timing decorator (exti / catch_timeit)

### Handler
  - [X] handle exceptions
    - [X] print stacktrace
    - [X] forward stacktrace to notifier
  - [X] handle timing results of functions
    - [ ] forward to notifier

### Notifier
#### BaseNotifier
  - [X] provide interface for extensions
  
#### HTTPNotifier
  - [X] send stacktrace via POST to specified url
  
#### SMTPNotifier
  - [X] send stacktrace via Mail to specified email addresses

### Rescuer
  - [ ] Manager like interface for threads / processes
  - [ ] Capture exceptions
  - [ ] Interface which accepts replacements
    - [ ] Socket
    - [ ] Webserver
  - [ ] Replace functions / classes
  
## usage
### basic

```python
import time
from exceptionalpy import catch, timeit, exceptionalpy_handler as handler

handler.verbose = True  # since you probably want to see your timing results


@timeit()
def gotta_work_fast():
  time.sleep(0.4)
  
  
@catch()
def cant_fail():
  raise ArithmeticError


gotta_work_fast()  
# gotta_work_fast completed in 400432710 ns | 400.43271 ms | 0.40043270999999997 s
cant_fail()
# prints stacktrace
print("I will still be printed.")
print("Since the program will not exit even though an exception occurred.")
```

### extensive guide
```python
import time
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


# there is also a timing decorator that catches the exception
from exceptionalpy import exti


@exti()
def i_take_a_moment_to_throw():
  time.sleep(0.6)
  print("Heyyyyy")
  raise ArithmeticError


# if you still want to time your functions and 
# have the result be forwarded to the notifier
from exceptionalpy import ti


@ti()
def i_take_a_moment():
  time.sleep(0.4)
  print("Slow function here, hi")
  
  
i_take_a_moment()
# upon successful execution, if you set the handlers verbose option to True,
# you will see something like this
# i_take_a_moment completed in 400432710 ns | 400.43271 ms | 0.40043270999999997 s
# and that result will be jsonified and forwarded to the notifier

# before any exceptions happen, you can also attach a notifier
from exceptionalpy.HTTP import HTTPNotifier

handler.notifier = HTTPNotifier("https://my-server:1337/api/exceptional", "POST")

# or just use a completely different handler
from exceptionalpy.SMTP import SMTPSHandler

handler = SMTPSHandler(("127.0.0.1", 25),  # which SMTP server to use
                       "exceptionalpy@locahost",  # the sender address
                       "dev@localhost",  # the receiver address
                       "There was an exception in your program")  # the subject
#  nothing bad will happen if you don't call
handler.deinit()
# beforehand. you can do it, but it's a waste of cpu cycles.

i_will_throw()
print("I will still be printed")
i_take_a_moment_to_throw()
print("I get printed as well since the program does not exit")
```