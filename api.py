from __future__ import print_function, unicode_literals
import os
from json import dumps

import requests

__author__ = 'sami'


class PushBullet(object):

    def __init__(self):
        self._devices = []
        self.retrieve_devices()
        self.valid_commands = ['note', 'link']

    @property
    def api_key(self):
        return os.environ.get('PUSHBULLET_API_KEY')

    @api_key.setter
    def api_key(self, value):
        os.putenv('PUSHBULLET_API_KEY', value)

    @property
    def user(self):
        response = requests.get(
            'https://api.pushbullet.com/v2/users/me',
            headers={
                'Access-Token': self.api_key
            })
        return response.json()

    @property
    def devices(self):
        if len(self._devices) == 0:
            self.retrieve_devices()
        return self._devices

    def push(self, command, device, msg):
        if command == 'note':
            self.push_note(' ', msg, device)
        elif command == 'link':
            split_msg = msg.split(' ')
            url = split_msg[0]
            body = '' if len(split_msg) == 1 else ' '.join(split_msg[1:])
            self.push_link(' ', body, url, device)

    def push_note(self, title, body, device):
        payload = dumps({
            'type': 'note',
            'title': title,
            'body': body,
            'device_iden': device.id
        })
        requests.post(
            'https://api.pushbullet.com/v2/pushes',
            data=payload,
            headers={
                'Access-Token': self.api_key,
                'Content-Type': 'application/json'
            })
        print('Pushed the note "{}" to {}'.format(body, device.name))

    def push_link(self, title, body, url, device):
        payload = dumps({
            'type': 'link',
            'title': title,
            'body': body,
            'url': url,
            'device_iden': device.id
        })
        requests.post(
            'https://api.pushbullet.com/v2/pushes',
            data=payload,
            headers={
                'Access-Token': self.api_key,
                'Content-Type': 'application/json'
            })
        print('Pushed the url "{}" to {}'.format(url, device.name))

    def retrieve_devices(self):
        request = requests.get(
            'https://api.pushbullet.com/v2/devices',
            headers={
                'Access-Token': self.api_key
            })
        json = request.json()
        for device in json['devices']:
            if device['active']:
                self._devices.append(Device(device))
        self._devices.append(AllDevice())
        self._devices = sorted(self._devices)


class Device(object):

    def __init__(self, json):
        self.json = json

    @property
    def name(self):
        return self.json['nickname']

    @property
    def type(self):
        return self.json['type']

    @property
    def id(self):
        return self.json['iden']

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '[{type}] {name}'.format(
            type=self.type.capitalize(),
            name=self.name
        )


class AllDevice(object):

    def __init__(self):
        pass

    @property
    def name(self):
        return 'all'

    @property
    def id(self):
        return ''

    def __lt__(self, other):
        return False

    def __str__(self):
        return '[Virtual Device] ALL'
