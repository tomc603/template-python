#!/usr/bin/env python3

#    Copyright 2022 Tom Cameron
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
This script is a template to be used as a sane default for new scripts. The
content should be modified for each new repository that is spawned from this
one.

TODO: Modify script file name
"""

import argparse
import logging
import os
import sys

SCRIPT_NAME = os.path.basename(sys.argv[0])

log_format = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
logger = logging.getLogger(SCRIPT_NAME)
logger.setLevel(logging.WARNING)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)


class ActionException(Exception):
    pass


def do_something(filepath: str, repeats: int) -> None:
    """Do the main work this script is supposed to perform.

    :param filepath: Path to a file that requires processing.
    :type filepath: str
    :param repeats: The number of times to do something to filepath.
    :type repeats: int
    """
    global logger

    try:
        logger.info(f'Doing something {repeats} times to filepath {filepath}.')
    except (OSError, IOError) as ex:
        logger.error(f'Low level exception occurred while doing something. {ex}.')
        raise ActionException('Caught a low level error')
    except (IndexError, AttributeError) as ex:
        logger.error(f'Attempted to access missing data while doing something. {ex}.')
        raise ActionException('Accessing data failed')


def main():
    """Handle the argument parsing and setup for this script's work."""

    global logger
    global console_handler

    parser = argparse.ArgumentParser(prog=SCRIPT_NAME, description='Template python script')
    args: argparse.Namespace

    try:
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-p', '--primary', action='store_true', help='Exclusive option A.')
        group.add_argument('-s', '--secondary', action='store_true', help='Exclusive option B.')
        parser.add_argument('-d', '--debug', action='store_true', help='Output developer messages while running.')
        parser.add_argument('-i', '--input', action='store', required=True, help='File containing data to read.')
        parser.add_argument('-S', '--syslog', action='store_true', help='Output messages to syslog.')
        parser.add_argument('-v', '--verbose', action='store_true', help='Output extra messages while running.')
        parser.add_argument('hosts', nargs='*', type=str, help='One or more hosts.')
        args = parser.parse_args()
    except argparse.ArgumentError as ex:
        logger.error(f'An error occurred while setting up argument parsing. {ex}.')
        sys.exit(1)
    except (argparse.ArgumentTypeError, TypeError) as ex:
        logger.error(f'An error occurred with an argument type. {ex}.')
        sys.exit(1)

    # Handle logging setup as early as possible
    if 'verbose' in args and args.verbose:
        logger.setLevel(logging.INFO)
        console_handler.setLevel(logging.INFO)

    if 'debug' in args and args.debug:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

    logger.debug(f'Arguments: primary: {args.primary}, secondary: {args.secondary}, '
                 f'debug: {args.debug}, input: {args.input}, verbose: {args.verbose} '
                 f'hosts: {args.hosts}')

    if not os.path.isfile(args.input):
        logger.error(f'File {args.input} is not a regular file or does not exist.')
        sys.exit(2)

    try:
        do_something(args.input, 10)
    except ActionException as ex:
        logger.error(f'Doing something failed. {ex}.')


if __name__ == '__main__':
    main()
