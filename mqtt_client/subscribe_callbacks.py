import subprocess


def default_subscribe_callback(mqttc, obj, msg):
    try:
        print(f'│{msg.topic}│ payload: {msg.payload}')
    except Exception as ex:
        print(f'Error: {ex}')


def subscribe_callback_raw(mqttc, obj, msg):
    try:
        print(msg.payload)
    except Exception as ex:
        print(f'Error: {ex}')


def subscribe_callback_command(command):
    def _(mqttc, obj, msg):
        response = subprocess.run(command.append(msg.payload), stdout=subprocess.PIPE)
        if response.stdout:
            print(response.stdout)
        if response.stderr:
            print(response.stderr)

    return _
