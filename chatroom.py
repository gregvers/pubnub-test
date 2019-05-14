#!/usr/bin/env python3

from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import datetime

def init_chatroom():
    pnconfig = PNConfiguration()
    pnconfig.publish_key = 'pub-c-c408ce7d-fe0d-4f9a-aae9-e67d5c9b6bd9'
    pnconfig.subscribe_key = 'sub-c-efaf056a-75c7-11e9-b68a-fa5eae84dea0'
    pubnub = PubNub(pnconfig)
    chatroom_listener = SubscribeListener()
    pubnub.add_listener(chatroom_listener)
    pubnub.subscribe().channels('mychatroom').execute()
    chatroom_listener.wait_for_connect()
    print('connected')
    return pubnub, listener

def post_msg(pubnub, nickname, msg):
    pubnub.publish().channel('mychatroom').message({'nickname': nickname, 'msg': msg, 'time': datetime.datetime.now()}).sync()

def get_msg(chatroom_listener):
    result = chatroom_listener.wait_for_message_on('mychatroom')
    print(result.message)


######## MAIN #########
def main(argv):
    parser = argparse.ArgumentParser(prog='chatroom', usage='%(prog)s nickname')
    parser.add_argument("nickname", type=str, action='store', help="nickname")
    args = parser.parse_args()
    if args.nickname == "":
        usage()
        sys.exit()

    pubnub, chatroom_listener = init_chatroom()



if __name__ == "__main__":
    main(sys.argv[1:])
