#  MIT License
#
#  Copyright (c) 2021 Pascal Eberlein
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

import sys
import traceback as tb


class BaseNotifier(object):
    def send(self, message: list[str]):
        pass


class Handler(object):
    _notifier: BaseNotifier = None

    def __init__(self, init: bool = True):
        if init:
            self._init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._deinit()

    def _init(self) -> None:
        sys.excepthook = self.handle_exception

    @staticmethod
    def _deinit() -> None:
        sys.excepthook = sys.__excepthook__

    def handle_exception(self, etype, value, traceback) -> None:
        exception = tb.format_exception(etype, value, traceback)
        for line in exception:
            print(line)

        if self._notifier is not None:
            self._notifier.send(exception)


__all__ = ["Handler", "BaseNotifier"]
