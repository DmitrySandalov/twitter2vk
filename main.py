import time
import ConfigParser

from pyvkoauth import auth
import vkontakte
from twitter import Twitter, OAuth

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

OAUTH_TOKEN = config.get('twitter-auth', 'OAUTH_TOKEN')
OAUTH_SECRET = config.get('twitter-auth', 'OAUTH_SECRET')
CONSUMER_KEY = config.get('twitter-auth', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('twitter-auth', 'CONSUMER_SECRET')
SCREEN_NAME = config.get('twitter-auth', 'SCREEN_NAME')

VK_EMAIL = config.get('vk-auth', 'VK_EMAIL')
VK_PASS = config.get('vk-auth', 'VK_PASS')
VK_CLIENT_ID = config.get('vk-auth', 'VK_CLIENT_ID')

UPDATE_TIMEOUT = config.get('other', 'UPDATE_TIMEOUT')


def get_vk_token():
    scope = 49151
    response = auth(VK_EMAIL, VK_PASS, VK_CLIENT_ID, scope)
    access_token = response['access_token']
    vk = vkontakte.API(token=access_token)
    token_expire_time = int(response['expires_in']) + vk.getServerTime()
    return access_token, token_expire_time, vk


def get_latest_tweet():
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET))
    return t.statuses.user_timeline(
        screen_name=SCREEN_NAME)[0]['text']


def get_latest_vk_status(vk):
    return vk.wall.get(count=1)[1]['text']


def main():
    expire_time = ''
    while True:
        local_time = int(time.time())
        if local_time > expire_time or expire_time == '':
            token, expire_time, vk = get_vk_token()
        latest_tweet = get_latest_tweet()
        latest_vk_status = get_latest_vk_status(vk)
        if latest_tweet != latest_vk_status:
            vk.wall.post(message=latest_tweet)
            print "Status updated", time.ctime(local_time)

        time.sleep(float(UPDATE_TIMEOUT))


if __name__ == "__main__":
    main()
