import requests
import json

# FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
# APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
# DOMAIN = 'rafagotest.a2hosted.com'


class EMAIL_HANDLER():
    def __init__(self, saveJsonData):
        self.saveJsonData = saveJsonData

        self.FROM = f'{self.saveJsonData["sender"]["value"]} <{self.saveJsonData["senderEmail"]["value"]}>'
        self.APIKEY = self.saveJsonData["apiKey"]["value"]
        self.DOMAIN = self.saveJsonData["domain"]["value"]
      
    def riskValidate(self, uiApp, email):
        check = requests.get(
            "https://api.mailgun.net/v4/address/validate",
            auth=("api", self.APIKEY),
            params={"address": email})
        risk = json.loads(check.content)['risk']

        if(risk != 'low'):
            uiApp.returnUiMessage(f'{email} is {risk} risk, sending failed.', 'Warning')
        else :
            uiApp.returnUiMessage(f'{email} is {risk} risk, start sending.')
        
        return True if risk == 'low' else False

    
    def sendtemplateMessage(self, uiApp, userData={'name', 'email', 'template', 'tag', 'subject'}):
          
        if ('name' and 'template' and 'email' and 'tag' and 'subject' in userData.keys()):

            if(self.riskValidate(uiApp, userData["email"])):

                post = requests.post(
                    f'https://api.mailgun.net/v3/{self.DOMAIN}/messages',
                    auth=('api', self.APIKEY),
                    data={'from': self.FROM,
                        'to': [userData['name'], f'<{userData["email"]}>'],
                        'subject':  userData["subject"],
                        'template': userData['template'],
                        't:variables': json.dumps({'name': userData["name"]}),
                        'o:tag': [userData["tag"]]
                        }
                )
            
                try:
                    message = json.loads(post.content)['message']
                    uiApp.returnUiMessage(f'{userData["email"]} : {message}')
                except:
                    uiApp.returnUiMessage('Mailgun setup error, please check if the api key and domain are correct', 'Warning')
                    return False
                    

