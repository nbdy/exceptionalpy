from exceptionalpy.SMTP import SMTPHandler
from smtpd import DebuggingServer


class TestServer(DebuggingServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(mailfrom)
        print(data)
        print("---------------------")


if __name__ == '__main__':
    a = ("127.0.0.1", 2525)
    print("Starting SMTP Server")
    s = TestServer(a, None)
    print("Starting SMTPHandler")
    h = SMTPHandler(a, "jeff@bezoz.ez", ["root@localhost"], "hi", True, debug=True)
    print("Raising exception")
    raise ArithmeticError
    print("The previous will be caught, but we still have to exit. This will not be printed")

