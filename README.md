# MQTT Client

ver: 1.7.0

[Documentation](https://mqtt.clubpulp.com/)

[![Downloads](https://pepy.tech/badge/mqtt-client)](https://pepy.tech/project/mqtt-client)
[![Downloads](https://pepy.tech/badge/mqtt-client/month)](https://pepy.tech/project/mqtt-client)
[![Downloads](https://pepy.tech/badge/mqtt-client/week)](https://pepy.tech/project/mqtt-client)

**mqtt-client** is a simple shell *MQTT client*.

Some of its essential features are: callback system, interactive publishing mode, TCP and Websockets support and configuration via json file.

## Install

> pip install --upgrade mqtt-client

## Examples

```shell
mqtt-client publish --config=my_config_file.json
mqtt-client subscribe --config=my_config_file.json
```

```shell
mqtt-client publish --host=mqttbroker.testing:1883 --topic=home/room/1/up --payload=ok
mqtt-client publish --host=mqttbroker.testing:1883 --topic=home/room/1/up --interactive
mqtt-client subscribe --host=mqttbroker.testing:1883 --topic=home/room/1/up
```

```shell
mqtt-client subscribe --host=mqttbroker.testing:1883 --topic=home/room/1/up --callback=command --options=/home/scripts/myScript.bash
```

## Usage

```shell
Usage:
  mqtt-client (publish | subscribe) --config=<config>
  mqtt-client publish --host=<host> --topic=<topic> (--payload=<payload> | --interactive) [--client_id=<client_id>] [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--qos=<qos>] [--retain=<retain>]
  mqtt-client subscribe --host=<host> --topic=<topic> [--client_id=<client_id>] [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--callback=<callback>] [--options=<options>]
  mqtt-client (-h|--help)
  mqtt-client (-v|--version)

Commands:
  publish                   Publish to topic from MQTT Broker.
  subscribe                 Subscribe to topic from MQTT Broker.

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
  --without_banner          Remove settings banner.
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
  --callback=<callback>     Use a custom callback for subscriber. (default, raw, limited, command)
  --options=<options>       Options for callback type command.
```

## Example file config

> mqtt-client publish --config=example_config.json

```json
{
    "host": "mqttbroker:1883",
    "topic": "my_topic",
    "payload": "Testing Simple MQTT Client",
    "interactive": false,
    "client_id": "awesome-mqtt-client",
    "username": "user",
    "password": "pass",
    "transport": "TCP",
    "cert_path": "",
    "qos": 0,
    "retain": false,
    "callback": "",
    "options": ""
}
```
