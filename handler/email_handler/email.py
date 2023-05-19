import requests
import json

# FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
# APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
# DOMAIN = 'rafagotest.a2hosted.com'



class EMAIL_HANDLER:
    def __init__(self, uiApp, loadJsonData, userData=None):
        
        # pass functions from parentNode. 
        self.uiApp = uiApp

        self.tagMailgun = loadJsonData['mailgun']
        self.tagTarget = loadJsonData['target']
        self.tagValidate = loadJsonData['validate']

        self.FROM = f'{self.tagMailgun["sender"]["value"]} <{self.tagMailgun["senderEmail"]["value"]}>'
        self.DOMAIN = self.tagMailgun["domain"]["value"]
        self.mailgunApiKey = self.tagMailgun["apiKey"]["value"]
        self.validateApiKey = self.tagValidate["v-apiKey"]["value"]
        self.userData = userData

    """
    validate email by millionverifier.
    """
    # @return Boolean.
    def riskValidate(self, email):

        url = f"https://api.millionverifier.com/api/v3/?api={self.validateApiKey}&email={email}&timeout=10"

        

        response = requests.request("GET", url)
        
        quality = json.loads(response.content)['quality']

        """
        3 levels of quality : Good, Bad, Risky.
        """
        # @return TRUE when quality is Good.
        if(quality != 'good'):
            self.uiApp.displayUiMessageHandler(f'{email} quality is {quality}, sending failed.', 'Warning')
            return False
        else :
            self.uiApp.displayUiMessageHandler(f'{email} quality is {quality}, start sending.')

        return True if quality == 'good' else False

    
    def sendtemplateMessage(self, userData={'name', 'email', 'template', 'analytics', 'subject'}, testMode = False):
        
        def sendHelper():
            post = requests.post(
                f'https://api.mailgun.net/v3/{self.DOMAIN}/messages',
                auth=('api', self.mailgunApiKey),
                data={'from': self.FROM,
                    'to': [userData['name'], f'<{userData["email"]}>'],
                    'subject':  userData["subject"],
                    'template': userData['template'],
                    't:variables': json.dumps({'name': userData["name"]}),
                    'o:tag': [userData["analytics"]]
                    }
            )

            message = json.loads(post.content)['message']
            self.uiApp.displayUiMessageHandler(f'{userData["email"]} : {message}')
        
          
        if ('name' and 'template' and 'email' and 'analytics' and 'subject' in self.tagTarget.keys()):

            if(testMode):
                sendHelper()
            else:
                sendHelper() if self.riskValidate(userData["email"]) else False
                
        else:
            return False


    def sendingEmails(self):

        excelData = self.userData

        num = 0
        if (excelData != False):
            state = True
            for i in excelData:
                name = i[1]
                email = i[3]
                userData = {'name': name,
                            'email': email,
                            'template': self.tagTarget['template']['value'],
                            'analytics': self.tagTarget['analytics']['value'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', name)
                            }
                
                sendState = self.sendtemplateMessage(userData)
                num = num + 1


                if (sendState == False):
                    num = num - 1
                    i.append('Failed')
                    # state = False
                    # break




        return {'state':state, 'num':num, 'userData':excelData }  
        
    def directSendEmails(self, email=None):

        if (email != None ):
            state = True
            num = 0
            for i in email:
                userData = {'name': 'test name',
                            'email': i,
                            'template': self.tagTarget['template']['value'],
                            'analytics': self.tagTarget['analytics']['value'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', 'test name')
                            }
                sendState = self.sendtemplateMessage(userData, testMode = True)
                num = num + 1
                if (sendState == False):
                    num = num - 1
                    state = False
                    break

            return {'state':state, 'num':num }    
                

