#!/usr/bin/env python

import re
from dataclasses import dataclass


@dataclass
class Field:
    pattern: str
    sep: str = r"\s*:\s*"  # E.g.: ' : '
    leading: str = r"\s*"
    specifier: str = None
    value: str = None
    optional: bool = False
    ignorecase: bool = False

    def __post_init__(self):
        if not self.specifier:
            self.specifier = self.pattern.lower().replace(" ", "_")
        if not self.value:
            self.value = r".*?"
        regstr = (
            rf"^{self.leading}"
            rf"{self.pattern}"
            rf"{self.sep}"
            rf"(?P<{self.specifier}>{self.value})\n"
        )
        if self.optional:
            # Turn the regular expression into a non-capturing group with
            # 0 or 1 repititions of the entire pattern.
            regstr = rf"(?:{regstr})?"
        self.regex = re.compile(regstr)


@dataclass
class Parser:
    fields: Field
    sep: str = ""

    def __post_init__(self):
        self.regex = re.compile(
            "%s" % (".*?".join(field.regex.pattern for field in self.fields)),
            re.MULTILINE | re.DOTALL,
        )

    def parse(self, string):
        """Iterate over each substring"""
        return [
            mtch.groupdict()
            for substr in re.split(self.sep, string)
            if (mtch := self.regex.search(substr))
        ]
