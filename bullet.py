#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from sys import argv

from prompt_toolkit.shortcuts import get_input

from api import PushBullet, Device, AllDevice
from completer import CommandCompleter
from exceptions import UnknownCommand, UnknownDevice

__author__ = 'sami'

help_string = 'All commands can be tab-completed on properly supported terminals\n' \
              'Valid commands:\n' \
              '    note      - Push a message to one or all of your devices\n' \
              '    link      - Push a link to one or all of your devices\n' \
              '    devices   - List all available devices\n' \
              '    help      - This message\n' \
              '    quit      - Quit interactive mode. Ctrl-C also works'


def parse(txt, device_list, command_list):
    """ Takes text from command line and gives the tuple of what command, whom it applies to, and the rest """

    command = None
    for c in command_list:
        if txt.startswith(c):
            command = c
            txt = txt[len(c)+1:]
            break
    if command is None:
        raise UnknownCommand()

    device = None
    for d in device_list:
        if txt.lower().startswith(d.name.lower()):
            device = d
            txt = txt[len(d.name)+1:]
            break
    if device is None:
        raise UnknownDevice()

    return command, device, txt


def main(args):
    pb = PushBullet()
    command_completer = CommandCompleter(pb)

    def loop(txt):
        if 'quit' == txt.lower():
            exit(0)
        elif 'devices' == txt.lower():
            for device in pb.devices:
                if not isinstance(device, AllDevice):
                    print(device)
        elif 'help' == txt.lower():
            print(help_string)
        elif '' == txt.lower():
            pass
        else:
            try:
                command, device, msg = parse(txt, pb.devices, pb.valid_commands)
                pb.push(command, device, msg)
            except UnknownCommand:
                print('Unknown command, try \'help\' for a list of valid ones')
            except UnknownDevice:
                print('Device name not recognized')

    if len(args) > 1:
        loop(' '.join(args[1:]))
        exit(0)

    try:
        while True:
            text = get_input('> ', completer=command_completer)
            loop(text)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main(argv)
