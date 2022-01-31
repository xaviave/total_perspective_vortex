import os
import re
import logging
import argparse
import itertools


class FileCheckerAction(argparse.Action):
    @staticmethod
    def _check_map(file_name: str):
        with open(file_name, "r") as f:
            fdata = list(
                filter(None, [re.match("[0-9 ]+", r) for r in f.read().split("\n")])
            )
        try:
            size = int(fdata[0].group())
        except ValueError:
            raise ValueError(f"Puzzle size too low")
        p = sorted(
            map(
                int,
                list(
                    itertools.chain(
                        *[list(filter(None, x.group().split(" "))) for x in fdata[1:]]
                    )
                ),
            )
        )
        if p != list(range(size ** 2)):
            raise ValueError(f"Bad number in Puzzle provided")
        logging.info("File is valid")

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.exists(values) or os.path.splitext(values)[1] != ".txt":
            raise ValueError(
                f"File '{values}' does not exist or is in the wrong format (TXT)"
            )
        self._check_map(values)
        setattr(namespace, self.dest, values)
