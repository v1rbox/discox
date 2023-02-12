[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

# Discox

Virbox Discord Bot community project ^\_^

Written in ~~blazingly fast~~ **effective** Python.

Documentation and installation guide can be found at our [wiki](https://github.com/v1rbox/discox/wiki) or [guide](#how-to-setup-very-simplified).

## How to setup

1. Install poetry (`pip install poetry`) and GNU make (should came with most linux distros or if windows then you can install it with winget by `winget install -e --id GnuWin32.Make`)
2. Clone Discox's repository
3. Run `make init`
4. Edit `.env` file with example provided in .env.example
5. Run your bot up with `make run`
6. If you want to add your own dependencies you could with `make add <package>` and to remove it you could with `make remove <package>` like pip
7. Read [wiki](https://github.com/v1rbox/discox/wiki) for how to create commands et cetera.

### Setting up the MySQL database

The bot relies on a MySQL database to function, to set it up you want to download MySQL / mariaDB

Then simply start / enable it with systemd

```
systemctl start mariadb
```

The client expects a user `root@localhost` with the password of `''` aka no password. It will automatically set everything up from there when running for the first time


## Contributors & Authors

[![contributors](https://contrib.rocks/image?repo=v1rbox/discox)](https://github.com/v1rbox/discox/graphs/contributors)
