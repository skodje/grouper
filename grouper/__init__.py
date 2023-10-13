#!/usr/bin/env python

import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Field:
    """Class to identify a key/value pair by regular expression.

    Arguments:
        pattern (str): Main pattern identifying the field to look for.
        separator (str): Pattern that separator the identifying string from the
            value.
        leading (str): Optional pattern indicating how the string starts.
        specifier (str): The regular expression group name.
        value (str): Regular expression identifying the value.
        optional (bool): Boolean indicating whether the field is optional.

    """
    pattern: str
    separator: str = r"\s*:\s*"
    leading: str = r"\s*"
    specifier: str = None
    value: str = None
    optional: bool = False

    def __post_init__(self) -> None:
        if not self.specifier:
            self.specifier = self.pattern.lower().replace(" ", "_")
        if not self.value:
            self.value = r".*?"
        regstr = (
            rf"^{self.leading}"
            rf"{self.pattern}"
            rf"{self.separator}"
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
    separator: str = r"^\s*$"  # (blank line)

    def __post_init__(self) -> None:
        self.regex = re.compile(
            "%s" % (".*?".join(field.regex.pattern for field in self.fields)),
            re.MULTILINE | re.DOTALL,
        )

    def parse(self, string: str) -> List[Dict[str, str]]:
        """Parse string and produce groupings.

        Iterate over each substring separated by our separator and turn them
        into a list of dicts based on our regular expressin.


        Arguments:
            string (str): The string to parse.

        Returns:
            list: A list of dicts.
        """
        return [
            mtch.groupdict()
            for substr in re.split(self.separator, string, flags=re.MULTILINE)
            if (mtch := self.regex.search(substr))
        ]
