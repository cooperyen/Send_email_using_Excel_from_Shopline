import requests
import json

FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
DOMAIN = 'rafagotest.a2hosted.com'


def riskValidate(uiApp, email):
    check = requests.get(
        "https://api.mailgun.net/v4/address/validate",
        auth=("api", APIKEY),
        params={"address": email})
    risk = json.loads(check.content)['risk']

    if(risk != 'low'):
        uiApp.returnUiMessage(f'{email} is {risk} risk, sending failed.', 'Warning')
    else :
        uiApp.returnUiMessage(f'{email} is {risk} risk, start sending.')
    
    return True if risk == 'low' else False

def sendtemplateMessage(uiApp, userData={'name', 'email', 'template', 'tag', 'subject'}):

    if ('name' and 'template' and 'email' and 'tag' and 'subject' in userData.keys()):

        if(riskValidate(uiApp, userData["email"])):

            post = requests.post(
                f'https://api.mailgun.net/v3/{DOMAIN}/messages',
                auth=('api', APIKEY),
                data={'from': FROM,
                    'to': [userData['name'], f'<{userData["email"]}>'],
                    'subject':  userData["subject"],
                    'template': userData['template'],
                    't:variables': json.dumps({'name': userData["name"]}),
                    'o:tag': [userData["tag"]]
                    }
            )
            message = json.loads(post.content)['message']

            uiApp.returnUiMessage(f'{userData["email"]} : {message}')

