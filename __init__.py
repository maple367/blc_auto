import os
import configparser
# environment variables
config = configparser.ConfigParser()
if os.path.exists('./local.config'):
    config.read('./local.config')
else:
    config.read('./config')
os.environ['OPENAI_API_KEY'] = config['API-KEY']['OPENAI_API_KEY']
url = config['LIVE']['DANMU_URL']
url_live = config['LIVE']['ROOM_URL']

if __name__ == '__main__':
    print(os.environ['OPENAI_API_KEY'])
    print(url)
    print(url_live)