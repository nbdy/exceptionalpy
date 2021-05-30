#  MIT License
#
#  Copyright (c) 2021. Pascal Eberlein
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import random
import time

from exceptionalpy import ti, ex, exceptionalpy_handler
from exceptionalpy.APIServer import APIServer
from procpy import Process


class TestApplication(Process):
    do_run: bool = True

    @ti()
    def timed_function(self):
        print("i get timed")
        time.sleep(random.randint(0, 4))

    @ex()
    def caught_function(self):
        print("i get caught")
        raise ArithmeticError("Oh no")

    def run(self) -> None:
        while self.do_run:
            self.caught_function()
            self.timed_function()
            time.sleep(2)


if __name__ == '__main__':
    exceptionalpy_handler = APIServer(debug=True)
    ta = TestApplication()

    try:
        print("starting testapplication")
        ta.start()
        print("starting api")
        exceptionalpy_handler.run()
        print("joining testapplication")
        ta.join()
    except KeyboardInterrupt:
        print("terminating")
        ta.terminate()
    print("done")
