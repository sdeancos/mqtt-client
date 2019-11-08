# MQTT Client 1.3.0

[![Downloads](https://pepy.tech/badge/mqtt-client)](https://pepy.tech/project/mqtt-client) [![Downloads](https://pepy.tech/badge/mqtt-client/month)](https://pepy.tech/project/mqtt-client) [![Downloads](https://pepy.tech/badge/mqtt-client/week)](https://pepy.tech/project/mqtt-client)

## Install

> pip install mqtt-client

## Usage

Simple MQTT Client.

```shell
Usage:
  mqtt-client (publish | subscribe) --config=<config>
  mqtt-client publish --host=<host> --topic=<topic> (--payload=<payload> | --interactive) [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--qos=<qos>] [--retain=<retain>]
  mqtt-client subscribe --host=<host> --topic=<topic> [--username=<username>] [--password=<password>] [--transport=<transport>] [--cert_path=<cert_path>] [--callback=<callback>] [--command=<command>]
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
  --username=<username>     Username.
  --password=<password>     Password.
  --transport=<transport>   TCP, TCP-TLS, WS, WS-TLS (Default: TCP)
  --cert_path=<cert_path>   Path cert (Default: ./mqtt_broker_cert.pem)
  --qos=<qos>               Qos (Default: 0)
  --retain=<retain>         Retain (Default: false)
  --callback=<callback>     Use a custom callback for subscriber. (default, raw, command)
  --command=<command>       Command for callback type command.

```

## Example file config

> $ mqtt-client publish --config=example_config.json

```json
{
  "host": "mqttbroker:1883",
  "topic": "my_topic",
  "payload": "Testing Simple MQTT Client 1.3.0",
  "interactive": false,
  "username": "user",
  "password": "pass",
  "transport": "TCP",
  "cert_path": "",
  "qos": 0,
  "retain": false,
  "callback": "",
  "command": ""
}
```