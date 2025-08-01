import subprocess


def default_subscribe_callback(mqttc, obj, msg):
    try:
        print(f'│{msg.topic}│ payload: {msg.payload.decode("utf8")}')
    except Exception as ex:
        print(f'Error: {ex}')


def subscribe_callback_limited(limit):
    limit = int(limit)

    def _(mqttc, obj, msg):
        try:
            print(f'│{msg.topic}│ payload: {msg.payload.decode("utf8")[:limit]}')
        except Exception as ex:
            print(f'Error: {ex}')

    return _


def subscribe_callback_raw(mqttc, obj, msg):
    try:
        print(msg.payload.decode('utf8'))
    except Exception as ex:
        print(f'Error: {ex}')


def subscribe_callback_command(command):
    command = command.split(' ')
    n = len(command)

    def _(mqttc, obj, msg):
        command.append(msg.topic)
        command.append(msg.payload.decode('utf8'))

        response = subprocess.run(command, stdout=subprocess.PIPE)
        if response.stdout:
            print(response.stdout.decode('utf8'))
        if response.stderr:
            print(response.stderr.decode('utf8'))
        command.pop(n)
        command.pop(n)

    return _
