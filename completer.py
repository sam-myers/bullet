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

        on_devices = line.startswith('note ') or line.startswith('url ')
        if on_devices:
            partial_device = document.get_word_before_cursor()
            auto_completion_devices = [d.name.lower() for d in self.pushbullet.devices]  # + ['all']
            completed_device_entered = False
            for device in auto_completion_devices:
                if device in line:
                    completed_device_entered = True

            if not completed_device_entered:
                for device in auto_completion_devices:
                    if device.startswith(partial_device):
                        yield Completion(device, -len(partial_device))
            else:
                yield Completion('Message to push', -len(partial_device))
