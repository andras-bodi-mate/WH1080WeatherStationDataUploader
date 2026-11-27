import argparse


class ArgumentNamespace(argparse.Namespace):
    username: str | None
    password: str | None
    failEarly: bool
    noUpload: bool
    quiet: bool
    verbose: bool
