import time
from multiprocessing import Process
from flask import Flask, request, make_response
from exceptionalpy.HTTP import HTTPGetHandler


def main():
    app = Flask(__name__)

    @app.route("/notify")
    def notify():
        data = request.json
        print(data)
        return make_response()

    app.run("127.0.0.1", 51341)


if __name__ == '__main__':
    print("Instantiated handler")
    h = HTTPGetHandler("http://127.0.0.1:51341/notify", verbose=True)
    print("Starting http server")
    p = Process(target=main)
    p.start()
    print("Sleeping")
    time.sleep(1)
    print("Raising exception")
    x = None
    x[3] = 3
    print("Joining http server")
    p.join(5)
    print("Terminating http server")
    p.terminate()
