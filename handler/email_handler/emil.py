import requests
import json

# FROM = 'RafaGo Rafa牽著吉娃娃 <service.rafago@gmail.com>'
# APIKEY = 'key-7317a30a70357cf6309ab4fead46637d'
# DOMAIN = 'rafagotest.a2hosted.com'


class EMAIL_HANDLER:
    def __init__(self, uiApp, loadJsonData, userData=None):
        self.tagMailgun = loadJsonData['mailgun']
        self.tagTarget = loadJsonData['target']
        self.uiApp = uiApp

        self.FROM = f'{self.tagMailgun["sender"]["value"]} <{self.tagMailgun["senderEmail"]["value"]}>'
        self.APIKEY = self.tagMailgun["apiKey"]["value"]
        self.DOMAIN = self.tagMailgun["domain"]["value"]
        self.userData = userData
      
    def riskValidate(self, email):

        url = f"https://api.millionverifier.com/api/v3/?api=Ob3F6xDemZzkFV4QVppLjzOvs&email={email}&timeout=10"

        response = requests.request("GET", url)
        
        quality = json.loads(response.content)['quality']

        # check = requests.get(
        #     "https://api.mailgun.net/v4/address/validate",
        #     auth=("api", self.APIKEY),
        #     params={"address": email})
        # risk = json.loads(check.content)['risk']


        if(quality != 'good'):
            self.uiApp.displayUiMessageHandler(f'{email} quality is {quality}, sending failed.', 'Warning')
            return False
        else :
            self.uiApp.displayUiMessageHandler(f'{email} quality is {quality}, start sending.')

        

        return True if quality == 'good' else False
        # return True
    
    def sendtemplateMessage(self, userData={'name', 'email', 'template', 'tag', 'subject'}):
          
        if ('name' and 'template' and 'email' and 'tag' and 'subject' in self.tagTarget.keys()):
  
            # try:
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
                    self.uiApp.displayUiMessageHandler(f'{userData["email"]} : {message}')

                else:
                    return False




            #     else:
            #         self.uiApp.displayUiMessageHandler(f'{userData["email"]} : False')
            #         return False
            # except:
            #     self.uiApp.displayUiMessageHandler('Mailgun setup error, please check if the api key and domain are correct', 'Warning')
            #     return False

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
                            'tag': self.tagTarget['tag']['value'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', 'test name')
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
                            'tag': self.tagTarget['tag']['value'],
                            'subject': self.tagTarget["subject"]["value"].replace('{name}', 'test name')
                            }
                sendState = self.sendtemplateMessage(userData)
                num = num + 1
                if (sendState == False):
                    num = num - 1
                    state = False
                    break

            return {'state':state, 'num':num }    
                

