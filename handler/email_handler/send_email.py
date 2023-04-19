import requests
import json

# FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
# APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
# DOMAIN = 'rafagotest.a2hosted.com'


class EMAIL_HANDLER():
    def __init__(self, loadJsonData):
        self.loadJsonData = loadJsonData

        self.FROM = f'{self.loadJsonData["sender"]["value"]} <{self.loadJsonData["senderEmail"]["value"]}>'
        self.APIKEY = self.loadJsonData["apiKey"]["value"]
        self.DOMAIN = self.loadJsonData["domain"]["value"]
        self.sentNum = 0
      
    def riskValidate(self, uiApp, email):
        check = requests.get(
            "https://api.mailgun.net/v4/address/validate",
            auth=("api", self.APIKEY),
            params={"address": email})
        risk = json.loads(check.content)['risk']

        if(risk != 'low'):
            uiApp.returnUiMessageHandler(f'{email} is {risk} risk, sending failed.', 'Warning')
        else :
            self.sentNum = self.sentNum + 1
            uiApp.returnUiMessageHandler(f'{email} is {risk} risk, start sending.')
        

        return True if risk == 'low' else False

    
    def sendtemplateMessage(self, uiApp, userData={'name', 'email', 'template', 'tag', 'subject'}):
          
        if ('name' and 'template' and 'email' and 'tag' and 'subject' in userData.keys()):
  
            try:
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
                    
                    message = json.loads(post.content)['message']
                    uiApp.returnUiMessageHandler(f'{userData["email"]} : {message}')
            except:
                uiApp.returnUiMessageHandler('Mailgun setup error, please check if the api key and domain are correct', 'Warning')
                return False
                    

