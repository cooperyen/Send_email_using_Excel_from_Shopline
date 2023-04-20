import requests
import json

# FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
# APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
# DOMAIN = 'rafagotest.a2hosted.com'


class EMAIL_HANDLER:
    def __init__(self, uiApp, loadJsonData, userData):
        self.tagMailgun = loadJsonData['mailgun']
        self.tagTarget = loadJsonData['target']
        self.uiApp = uiApp

        self.FROM = f'{self.tagMailgun["sender"]["value"]} <{self.tagMailgun["senderEmail"]["value"]}>'
        self.APIKEY = self.tagMailgun["apiKey"]["value"]
        self.DOMAIN = self.tagMailgun["domain"]["value"]
        self.userData = userData
      
    def riskValidate(self, email):
        check = requests.get(
            "https://api.mailgun.net/v4/address/validate",
            auth=("api", self.APIKEY),
            params={"address": email})
        risk = json.loads(check.content)['risk']

        if(risk != 'low'):
            self.uiApp.returnUiMessageHandler(f'{email} is {risk} risk, sending failed.', 'Warning')
            return False
        else :
            self.uiApp.returnUiMessageHandler(f'{email} is {risk} risk, start sending.')

        

        return True if risk == 'low' else False
    
    def sendtemplateMessage(self, userData={'name', 'email', 'template', 'tag', 'subject'}):
          
        if ('name' and 'template' and 'email' and 'tag' and 'subject' in self.tagTarget.keys()):
  
            try:
                if(self.riskValidate(userData["email"])):

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
                    self.uiApp.returnUiMessageHandler(f'{userData["email"]} : {message}')
                else:
                    return False
            except:
                self.uiApp.returnUiMessageHandler('Mailgun setup error, please check if the api key and domain are correct', 'Warning')
                return False

    def sendingEmails(self):

        excelData = self.userData

        if (excelData != False):
            state = True
            for i in excelData:
                name = i[1]
                email = i[3]
                num = 0
                userData = {'name': name,
                            'email': email,
                            'template': self.tagTarget['template'],
                            'tag': self.tagTarget['tag'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', 'test name')
                            }
                
                sendState = self.sendtemplateMessage(userData)
                i.append(self.tagTarget['tag'])
                num = num + 1
                if (sendState == False):
                    num = num - 1
                    state = False
                    break

            return {'state':state, 'num':num }  
        
    def directSendEmails(self, email=None):

        if (email != None ):
            state = True
            num = 0
            for i in email:
                userData = {'name': 'test name',
                            'email': i,
                            'template': self.tagTarget['template'],
                            'tag': self.tagTarget['tag'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', 'test name')
                            }
                sendState = self.sendtemplateMessage(userData)
                num = num + 1
                if (sendState == False):
                    num = num - 1
                    state = False
                    break

            return {'state':state, 'num':num }    
                

