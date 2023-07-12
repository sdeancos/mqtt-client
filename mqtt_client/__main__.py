#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
  mqtt-client (publish | subscribe) --config=<config>
  mqtt-client publish --host=<host> --topic=<topic> (--payload=<payload> | --interactive) [--client_id=<client_id>] [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--qos=<qos>] [--retain=<retain>]
  mqtt-client subscribe --host=<host> --topic=<topic> [--client_id=<client_id>] [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--callback=<callback>] [--command=<command>]
  mqtt-client (-h|--help)
  mqtt-client (-v|--version)

Commands:
  publish                   Publish to topic from MQTT Broker.
  subscribe                 Subscribe to topic from MQTT Broker.

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
  --config=<config>         Config file.
  --host=<host>             Broker Host. (Example: example.your_broker.com:1883)
  --topic=<topic>           Topic.
  --payload=<payload>       Payload to send.
  -i --interactive          Interactive mode.
  --client_id=<client_id>   Client ID.
  --username=<username>     Username.
  --password=<password>     Password.
  --transport=<transport>   TCP, TCP-TLS, WS, WS-TLS (Default: TCP)
  --cert_path=<cert_path>   Path cert (Default: ./mqtt_broker_cert.pem)
  --qos=<qos>               Qos (Default: 0)
  --retain=<retain>         Retain (Default: false)
  --callback=<callback>     Use a custom callback for subscriber. (default, raw, command)
  --command=<command>       Command for callback type command.

"""
from docopt import docopt
import readline
import json

from terminaltables import SingleTable

from mqtt_client import mqtt_client

NAME, VERSION = 'MQTT Client', '1.6.1'
AUTHOR = 'Samuel de Ancos (2018-2023) <https://github.com/sdeancos/mqtt-client>'


def main():
    arguments = docopt(f'{NAME} {VERSION}\n{AUTHOR}\n\n{__doc__}', version=f'{NAME} {VERSION}')

    config = None
    if arguments['--config']:
        with open(arguments['--config']) as f:
            _config_content = f.read()
        config = json.loads(_config_content)
        host, port = config.get('host', 'localhost:1883').split(':')
        port = int(port)
        topic = config.get('topic')
        client_id = config.get('client_id', False)
        transport = config.get('transport', 'TCP')
        path = config.get('cert_path')
        username, password = config.get('username'), config.get('password')
        callback, command = config.get('callback'), config.get('command')
    else:
        host, port = 'localhost', 1883
        topic = None
        client_id = False
        transport = 'TCP'
        path = None
        username, password = None, None
        callback, command = None, None

    if arguments['--host']:
        try:
            host, port = arguments['--host'].split(':')
        except Exception:
            exit('│ERROR│ broker host failed. Example: example.your_broker.com:1883')
        if port:
            port = int(port)

    if '--client_id' in arguments and arguments['--client_id']:
        client_id = arguments['--client_id']

    if '--transport' in arguments and arguments['--transport']:
        transport = arguments['--transport']

    if '--cert_path' in arguments and arguments['--cert_path']:
        path = arguments['--cert_path']

    if '--username' in arguments and arguments['--username']:
        username = arguments['--username']

    if '--password' in arguments and arguments['--password']:
        password = arguments['--password']

    if '--callback' in arguments and arguments['--callback']:
        callback = arguments['--callback']

    if '--command' in arguments and arguments['--command']:
        command = arguments['--command']

    print(SingleTable([[NAME, VERSION]]).table)

    if not topic:
        topic = arguments['--topic']

    try:
        mqtt_handler = mqtt_client.connect_to_broker(
            host=host,
            port=port,
            topic=topic,
            client_id=client_id,
            username=username,
            password=password,
            transport=transport,
            cert_path=path
        )
        mqtt_handler.connect()
    except Exception as ex:
        exit(f'│ERROR│ {ex}')

    if arguments['publish']:
        if config and 'qos' in config:
            qos = config.get('qos', 0)
        else:
            qos = 0
            if '--qos' in arguments and arguments['--qos']:
                qos = int(arguments['--qos'])

        if config and 'retain' in config:
            retain = bool(config.get('retain', False))
        else:
            retain = 0
            if '--retain' in arguments and arguments['--retain']:
                retain = bool(arguments['--retain'])

        if (config and not 'interactive' in config) or not arguments['--interactive']:
            if config and 'payload' in config:
                payload = config['payload']
            elif '--payload' in arguments:
                payload = arguments['--payload']
            else:
                exit(f'│ERROR│ Not payload defined')

            is_published = mqtt_client.publish(mqtt_handler=mqtt_handler, payload=payload, qos=qos, retain=retain)
        else:
            mqtt_handler.loop_start()
            exit_by = ''
            while True:
                try:
                    payload = input('[insert payload] ? ')
                    is_published = mqtt_client.publish(mqtt_handler=mqtt_handler, payload=payload,
                                                       qos=qos, retain=retain)
                except KeyboardInterrupt:
                    exit_by = '[CTRL+C] Exit'
                    break
                except EOFError:
                    exit_by = '[CTRL+D] Exit'
                    break

            mqtt_handler.loop_stop()

            if exit_by is not '':
                exit(exit_by)

    if arguments['subscribe']:
        mqtt_client.subscribe(mqtt_handler=mqtt_handler, callback=callback, command=command)

if __name__ == '__main__':
    main()
