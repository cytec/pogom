#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import os
import sys
import uuid
import sys
import platform
import logging
from datetime import datetime, timedelta

from . import config

log = logging.getLogger(__name__)


def parse_unicode(bytestring):
    decoded_string = bytestring.decode(sys.getfilesystemencoding())
    return decoded_string


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='Set web server listening host', default='127.0.0.1')
    parser.add_argument('-P', '--port', type=int, help='Set web server listening port', default=5000)

    parser.add_argument('-d', '--debug', type=str.lower, help='Debug Level [info|debug]', default=None)

    parser.add_argument('-s', '--scan-only', help='start only the scanner, no webserver', action='store_true')

    parser.add_argument('--db-type', help='Type of database to be used (default: sqlite)', default='sqlite')
    parser.add_argument('--db-name', help='Name of the database to be used')
    parser.add_argument('--db-user', help='Username for the database')
    parser.add_argument('--db-pass', help='Password for the database')
    parser.add_argument('--db-host', help='IP or hostname for the database')

    args = parser.parse_args()
    if args.password is None:
        args.password = getpass.getpass()

    return args


def get_pokemon_name(pokemon_id):
    if not hasattr(get_pokemon_name, 'names'):
        file_path = os.path.join(
                config['ROOT_PATH'],
                config['LOCALES_DIR'],
                'pokemon.{}.json'.format(config['LOCALE']))

        with open(file_path, 'r') as f:
            get_pokemon_name.names = json.loads(f.read())

    return get_pokemon_name.names[str(pokemon_id)]


def get_encryption_lib_path():
    lib_folder_path = os.path.join(
        os.path.dirname(__file__), "lib")
    lib_path = ""
    # win32 doesn't mean necessarily 32 bits
    if sys.platform == "win32":
        if platform.architecture()[0] == '64bit':
            lib_path = os.path.join(lib_folder_path, "encrypt64bit.dll")
        else:
            lib_path = os.path.join(lib_folder_path, "encrypt32bit.dll")

    elif sys.platform == "darwin":
        lib_path = os.path.join(lib_folder_path, "libencrypt-osx-64.so")

    elif os.uname()[4].startswith("arm") and platform.architecture()[0] == '32bit':
        lib_path = os.path.join(lib_folder_path, "libencrypt-linux-arm-32.so")

    elif sys.platform.startswith('linux'):
        if platform.architecture()[0] == '64bit':
            lib_path = os.path.join(lib_folder_path, "libencrypt-linux-x86-64.so")
        else:
            lib_path = os.path.join(lib_folder_path, "libencrypt-linux-x86-32.so")

    elif sys.platform.startswith('freebsd-10'):
        lib_path = os.path.join(lib_folder_path, "libencrypt-freebsd10-64.so")

    else:
        err = "Unexpected/unsupported platform '{}'".format(sys.platform)
        log.error(err)
        raise Exception(err)

    if not os.path.isfile(lib_path):
        err = "Could not find {} encryption library {}".format(sys.platform, lib_path)
        log.error(err)
        raise Exception(err)

    return lib_path
