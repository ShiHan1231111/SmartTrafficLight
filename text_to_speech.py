from gtts import gTTS
from playsound import playsound
import os.path
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# It is a text value that we want to convert to audio  
prompt = input('Please text a message: ')
reportFileName = input('Insert the report time with your name (eg:11-11-2021-yeechooili)：')

# Here are converting in Malay Language
language = 'id'

# Passing the text and language to the engine,  
# here we have assign slow=False. Which denotes  
# the module that the transformed audio should  
# have a high speed  
obj = gTTS(text=prompt, lang=language, slow=False)

save_path = r'C:\Users\User\Desktop\Part1\audio'

filename = os.path.join(save_path, reportFileName + ".mp3")

obj.save(filename)

playsound(filename)