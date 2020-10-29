
from __future__ import annotations
from farmer.reporting.report import Report
from typing import Dict, List, Type, Union

TITLE = "="

HEADING = [
    TITLE,
    "=",
    "-",
    "^",
    "*"
]

class RstReporter(Report):

    def __init__(self, filename: str):
        self._doc = ""
        super(RstReporter, self).__init__(filename)
        self.title(self.filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    def _sanitize(self, text: str):
        cleaned = text.replace("<p>", "").replace("</p>", "").replace("&nbsp;", "\n").replace("\n\n", "\n")
        return cleaned.replace("\n\n", "\n")

    def _append(self, text):
        self._doc += self._sanitize(text)

    def line(self, text=""):
        self._append("{}\n".format(text))

    def directive(self, name: Union[str, Dict[str, str]], configs: List[Union[str, Dict[str, str]]]):
        self.line()
        if isinstance(name, str):
            self.line(".. {}::".format(name))
        elif isinstance(name, dict):
            for key in name:
                self.line(".. {}:: {}".format(key, name[key]))
        if configs:
            for config in configs:
                if isinstance(config, str):
                    self.line("    :{}:".format(config))
                elif isinstance(config, dict):
                    for key in config:
                        self.line("    :{}: {}".format(key, config[key]))
        self.line()

    def title(self, text: str):
        self.line(TITLE * len(text))
        self.line(text)
        self.line(TITLE * len(text))
        self.line()

    def heading(self, text: str, level: int):
        self.line()
        self.line(text)
        self.line(HEADING[level] * len(text))
        self.line()

    def lists(self, items: List[str], ordered=True):
        denote = "#" if ordered else "-"
        self.line()
        for item in items:
            self.line("{} {}".format(denote, item))
        self.line()

    def definition(self, key: str, term: str):
        self.line(":{}: {}".format(key, term))

    def toctree(self, depth=1):
        self.directive("contents", ["local", {"depth": depth}])

    def pagebreak(self):
        self.directive({"raw": "pdf"})
        self.line("    PageBreak")
        self.line()

    def save(self, pdf=False):
        path = "{}.rst".format(self.filename) if not self.filename.endswith(".rst") else self.filename
        with open(path, 'w') as rst:
            rst.write(self._doc)
