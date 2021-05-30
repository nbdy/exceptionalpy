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

from flask import Flask, request, make_response, jsonify
from exceptionalpy import Handler


class ExceptionHolder(object):
    exception = None
    func = None
    args = None
    kwargs = None

    def __init__(self, exception, func, *args, **kwargs):
        self.exception = exception
        self.func = func
        self.args = args
        self.kwargs = kwargs


class TimingHolder(object):
    func = None
    begin: int = None
    end: int = None
    duration: int = None
    args = None
    kwargs = None

    def __init__(self, func, begin, end, *args, **kwargs):
        self.func = func
        self.begin = begin
        self.end = end
        self.args = args
        self.kwargs = kwargs
        self.duration = end - begin


class DiagnosticsHolder(object):
    exceptions: list[ExceptionHolder] = None
    timings: list[TimingHolder] = None

    def __init__(self):
        self.exceptions = []
        self.timings = []

    def contains(self, exception) -> bool:
        for e in self.exceptions:
            if exception == e.exception:
                return True
        return False

    def add_exception(self, exception: ExceptionHolder) -> bool:
        if self.contains(exception.exception):
            return False
        self.exceptions.append(exception)
        return True

    def add_timing(self, timing: TimingHolder):
        self.timings.append(timing)

    def exception_count(self):
        return len(self.exceptions)

    def timing_count(self):
        return len(self.timings)


class APIServer(Handler):
    app: Flask = None
    data: DiagnosticsHolder = None

    # --- Overrides ---
    def handle_exception(self, exception, fn, *args, **kwargs) -> None:
        print("ayoooo")
        self.data.add_exception(ExceptionHolder(exception, fn, *args, **kwargs))
        # Handler.handle_exception(self, exception, fn, *args, **kwargs)

    def handle_timeit(self, fn, begin, end, *args, **kwargs):
        print("ayoooo")
        self.data.add_timing(TimingHolder(fn, begin, end, *args, **kwargs))
        # Handler.handle_timeit(self, fn, begin, end, *args, **kwargs)

    def __init__(self, host: str = "127.0.0.1", port: int = 4477, debug: bool = False):
        Handler.__init__(self, verbose=debug)
        self.host = host
        self.port = port
        self.debug = debug

        self.data = DiagnosticsHolder()

        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        self._register_api_routes()

    def _register_api_routes(self):
        self.app.add_url_rule("/api/replace", "api_replace", self.api_replace, methods=["POST"])
        self.app.add_url_rule("/api/exception/count", "api_exception_count", self.api_exception_count, methods=["GET"])
        self.app.add_url_rule("/api/timing/count", "api_timing_count", self.api_timing_count, methods=["GET"])
        self.app.add_url_rule("/api/exception/list", "api_exception_list", self.api_exception_list, methods=["GET"])
        self.app.add_url_rule("/api/timing/list", "api_timing_list", self.api_timing_list, methods=["GET"])

    def run(self) -> None:
        self.app.run(self.host, self.port, self.debug)

    # ------ Internal -------
    def _replace(self, data: dict):
        return False  # TODO

    # ------- Static --------
    @staticmethod
    def _make_jrsp(data: dict):
        return make_response(jsonify(data))

    # --------- API ---------
    def api_exception_count(self):
        return self._make_jrsp({
            "count": self.data.exception_count()
        })

    def api_timing_count(self):
        return self._make_jrsp({
            "count": self.data.timing_count()
        })

    def api_exception_list(self):
        return self._make_jrsp({
            "list": self.data.exceptions
        })

    def api_timing_list(self):
        return self._make_jrsp({
            "list": self.data.timings
        })

    def api_replace(self):
        data = request.get_json()
        rsp = {"error": True}
        if data is not None:
            rsp["error"] = not self._replace(data)
        return self._make_jrsp(rsp)
