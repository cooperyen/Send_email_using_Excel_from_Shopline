

import json

saveJsonFileName = 'setting.json'

class JASON_HANDLER():

    def writeJsonFile(data):
        with open(saveJsonFileName, 'w') as json_file:
            json.dump(data, json_file)

        json_file.close()

    def loadJasonFile():
        with open(saveJsonFileName, 'r') as json_file:
            return json.load(json_file)