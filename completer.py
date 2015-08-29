__author__ = 'sami'

from prompt_toolkit.completion import Completer, Completion


class CommandCompleter(Completer):

    def __init__(self, pushbullet):
        self.pushbullet = pushbullet
        self.commands = [
            'devices',
            'note',
            'link',
            'help',
            'quit'
        ]

    def get_completions(self, document, complete_event):
        line = document.current_line.lower()

        on_command = ' ' not in line
        if on_command:
            for command in self.commands:
                if command.startswith(line):
                    yield Completion(command, -len(line))

        in_note = line.startswith('note ')
        in_link = line.startswith('link ')
        on_devices = in_note or in_link
        if on_devices:
            partial_device = document.get_word_before_cursor()
            auto_completion_devices = [d.name.lower() for d in self.pushbullet.devices]
            completed_device_entered = False
            remaining_line = line[5:]
            for device in auto_completion_devices:
                if device in line:
                    completed_device_entered = True
                    remaining_line = remaining_line[len(device)+1:]
                    break

            if not completed_device_entered:
                for device in auto_completion_devices:
                    if device.startswith(partial_device):
                        yield Completion(device, -len(partial_device))
            else:
                if in_note:
                    yield Completion('', -len(partial_device), 'Message to push')
                elif in_link:
                    if ' ' not in remaining_line:
                        yield Completion('', -len(partial_device), 'URL to push')
                    else:
                        yield Completion('', -len(partial_device), '[Optional] Message to push')
