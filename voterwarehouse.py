# -*- coding: utf-8 -*-
import argparse
import importlib
import os

from Warehouse.version import __version__
from Warehouse.ImplementedStates import __implemented_states__

# VoterWarehouse command-line Voter and Voter History handling tool


def import_type(args: argparse.Namespace) -> None:
    """
    import_type Initializes conditional importing workflows based on what type was requested

    :param argparse.Namespace args: Argument dictionary to be evaluated by import types
    :return: None
    """
    try:
        if args.state in __implemented_states__:
            if os.path.isfile(args.config):
                with getattr(
                    importlib.import_module(f"Warehouse.{args.state}"),
                    f"{args.state}"
                )(args.config) as state_db:
                    with getattr(
                        importlib.import_module(f"Import.{args.state}"),
                        f"{args.state}"
                    )(state_db) as state:
                        if args.file is not None:
                            if os.path.isfile(args.file):
                                if args.type in state.valid_import_types.keys():
                                    state.import_source(
                                        args.file,
                                        args.type
                                    )
                                else:
                                    raise ValueError(f"Usage: Type {args.type} is not valid")
                            else:
                                raise FileExistsError(f"Usage: File {args.file} must exist!")
                        else:
                            raise ValueError(f"Usage: File must be provided")
            else:
                raise FileExistsError(f"Usage: Config File must exist!")
        else:
            raise ValueError(f"Usage: State {args.state} is not implemented")
    except Exception as error:
        print('Caught this error: ' + repr(error))
        raise


def main(args: argparse.Namespace) -> None:
    """
    main Sets up the conditional actions workflow based on the specified action

    :param argparse.Namespace args: Argument dictionary to be evaluated by action types
    :return: None
    """
    try:
        match args.action:
            case "import":
                if args.file is not None:
                    import_type(args)
                else:
                    raise ValueError(f"Usage: File must be provided")
            case _:
                raise ValueError(f"Usage: Action {args.action} is not valid")
    except Exception as error:
        print('Caught this error: ' + repr(error))
        raise


if __name__ == '__main__':
    """
    __name__ Initializes the application and parses the parameters

    :return: None
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s",
            "--state",
            help="The State Name",
            default="Florida"
        )
        parser.add_argument(
            "-a",
            "--action",
            help="Action"
        )
        parser.add_argument(
            "-t",
            "--type",
            help="Type"
        )
        parser.add_argument(
            "-f",
            "--file",
            help="File"
        )
        parser.add_argument(
            "-c",
            "--config",
            help="Config YAML File",
            default="/etc/VoterWarehouse/config.yml"
        )
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=__version__
        )
        try:
            main(parser.parse_args())
        except KeyboardInterrupt:
            print("\nShutdown by keyboard interrupt...exiting")
    except Exception as e:
        print('Caught this error: ' + repr(e))
        raise
