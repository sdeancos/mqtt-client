import ssl, time
from pathlib import Path

import random
import string

import paho.mqtt.client as mqtt
from terminaltables import SingleTable

from mqtt_client.subscribe_callbacks import (
    default_subscribe_callback,
    subscribe_callback_raw,
    subscribe_callback_command,
)

CERT_DEFAULT_PATH = 'mqtt_broker_cert.pem'
CONNECT_MQTT_BROKER = False
TIMEOUT_DEFAULT = 5


class MqttWrapper:
    def __init__(self, host, port, topic, auth, client_id=False, transport='tcp'):
        self.host = host
        self.port = port
        self.auth = auth
        self.timeout = TIMEOUT_DEFAULT
        self.topic = topic
        self._set_transport(transport=transport)
        self.cert_path = CERT_DEFAULT_PATH

        clean_session = False
        if client_id is False:
          client_id = 'mqtt-client-' + ''.join(random.choice(string.ascii_lowercase) for i in range(6))
          clean_session = True

        self.client_id = client_id
        self.client = mqtt.Client(self.client_id, clean_session, transport=self.transport)
        self.client.on_connect = self.on_connect

    def _set_transport(self, transport):
        if 'TCP' == transport or 'tcp' == transport:
            self.transport, self.tls = 'tcp', False
        elif 'TCP-TLS' == transport or 'tcp-tls' == transport:
            self.transport, self.tls = 'tcp', True
        elif 'WS' == transport or 'ws' == transport:
            self.transport, self.tls = 'websocket', False
        elif 'WS-TLS' == transport or 'ws-tls' == transport:
            self.transport, self.tls = 'websocket', True

    def set_tls(self, cert_path=None):
        if cert_path:
            self.cert_path = cert_path
        my_file = Path(self.cert_path)
        if not my_file.is_file():
            self.cert_path = None

        self.client.tls_set(self.cert_path, certfile=None, keyfile=None,
                            cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)

        # print(f'- SET TLS: {self.cert_path}')

    def connect(self):
        if 'username' in self.auth and 'password' in self.auth:
            if self.auth['username'] and self.auth['password']:
                self.client.username_pw_set(username=self.auth['username'], password=self.auth['password'])
        self.client.connect(self.host, self.port, self.timeout)

    def on_message(self, func):
        self.client.on_message = func

    def on_connect(self, mqttc, obj, flags, rc):
        if rc != 0:
            print('│ERROR│ from connect - rc: {}'.format(rc))

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop(force=False)

    def loop_forever(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            exit('│CTRL+C│ Exit by KeyboardInterrupt')

    def publish(self, payload, qos=0, retain=False):
        try:
            message_info = self.client.publish(self.topic, payload=payload, qos=qos, retain=retain)
            message_info.wait_for_publish()
            return message_info.is_published()
        except Exception as ex:
            exit(ex)


def connect_to_broker(host, port, topic, username, password, client_id=False, transport='tcp', cert_path=None):
    mqtt_handler = MqttWrapper(
        host=host,
        port=port,
        topic=topic,
        auth={'username': username, 'password': password},
        client_id=client_id,
        transport=transport
    )

    table_data = [
        ['KEY', 'VALUE'],
        ['BROKER SETTINGS', f'{transport}://{host}:{port}'],
        ['CREDENTIALS USER/PASSWORD', f'{username if username else "-"} {password if password else "-"}'],
        ['CLIENT-ID', f'{mqtt_handler.client_id}'],
        ['TOPIC', f'{topic}']
    ]

    print(SingleTable(table_data).table)

    if mqtt_handler.tls:
        if cert_path:
            mqtt_handler.set_tls(cert_path=cert_path)
        else:
            mqtt_handler.set_tls()

    return mqtt_handler


def publish(mqtt_handler, payload, qos=0, retain=False):
    is_published = mqtt_handler.publish(payload=str(payload), qos=qos, retain=retain)
    table_data = [[f'publish to {mqtt_handler.topic}', payload, 'Published: OK' if is_published else False]]
    print(SingleTable(table_data).table)

    return is_published


def subscribe(mqtt_handler, callback, command):
    mqtt_handler.client.subscribe(mqtt_handler.topic)

    if not callback or callback == 'default':
        callback = default_subscribe_callback

    if callback == 'raw':
        callback = subscribe_callback_raw

    if callback == 'command' and command:
        callback = subscribe_callback_command(command=command)

    mqtt_handler.on_message(func=callback)

    table_data = [[f'waiting from {callback}', '...']]
    print(SingleTable(table_data).table)
    mqtt_handler.loop_forever()
