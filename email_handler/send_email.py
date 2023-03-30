import requests
import json

FROM = 'RafaGo Rafa牽著吉娃娃 <cooper.rafago@gmail.com>'
APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
DOMAIN = 'rafagotest.a2hosted.com'


name = 'SHAO HSUAN YEN'

userData = {'name': name,
            'email': 'cooper.rafago@gmail.com',
            'template': 'test',
            'tag': 'only one order',
            'subject': f'subjectsubject {name}'
            }


def send_template_message(userData={'name', 'email', 'template', 'tag', 'subject'}):

    if ('name' and 'templates' and 'email' and 'tag' and 'subject' in userData.keys()):

        return requests.post(
            f'https://api.mailgun.net/v3/{DOMAIN}/messages',
            auth=('api', APIKEY),
            data={'from': FROM,
                  'to': [userData['name'], f'<{userData["email"]}>'],
                  'subject':  userData["subject"],
                  'template': userData['template'],
                  't:variables': json.dumps({'name': userData["name"]}),
                  'o:tag': [userData["name"]]
                  }
        )

    else:
        print('fail')


# send_template_message(userData)
