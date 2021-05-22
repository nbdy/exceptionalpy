import time

from exceptionalpy.SMTP import SMTPHandler
from smtpd import DebuggingServer
from multiprocessing import Process


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
    SMTPHandler(a, "jeff@bezoz.ez", ["root@localhost"], "hi")
    print("Raising exception")
    x = None
    x[2] = 2
    print("Sleeping for a second")
    time.sleep(1)
    print("Closing SMTP server")
    s.close()
