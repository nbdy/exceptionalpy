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