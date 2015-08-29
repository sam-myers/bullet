[![Build Status](https://travis-ci.org/Demotivated/bullet.svg?branch=master)](https://travis-ci.org/Demotivated/bullet)

### About PushBullet

[PushBullet](https://www.pushbullet.com/) is a services which allows one to quickly and easily send notifications / links / files between your devices. GUI-based clients already exist, this is an attempt to make a solid and simple CLI.

## Setup

```
pip install prompt-toolkit, requests
```

The first time it's run, Bullet will prompt you for your [access token](https://www.pushbullet.com/#settings/account). 

## Examples

![List devices](https://i.imgur.com/3ftBgnv.gif)

![Push a note](https://i.imgur.com/ByHeg62.gif)

Commands can also be invoked directly

```
bullet.py note computer name message
```

_Note that device names can and should be typed with spaces, quotes are not necessary_


## Upcoming Features

- File transfers
- SMS