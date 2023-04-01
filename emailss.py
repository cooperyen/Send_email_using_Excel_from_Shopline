
import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/rafagotest.a2hosted.com/messages",
        auth=("api", "key-7317a30a70357cf6309ab4fead46637d"),
        data={"from": "RafaGo <cooper.rafago@gmail.com>",
              "to": "SHAO HSUAN YEN <dknick081@gmail.com>",
              "subject": "Hello SHAO HSUAN YEN",
              "template": "test",
                    "h:X-Mailgun-Variables": "{'test': 'test'}"})


send_simple_message()
