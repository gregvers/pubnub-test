#!/usr/bin/env python3

import sys
import argparse
from pubnub.enums import PNOperationType, PNStatusCategory, PNReconnectionPolicy
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
import datetime, json

pubkey = 'pub-c-c408ce7d-fe0d-4f9a-aae9-e67d5c9b6bd9'
subkey = 'sub-c-efaf056a-75c7-11e9-b68a-fa5eae84dea0'

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print('connected')
        elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pubnub.reconnect()
            print('reconnected')
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            pubnub.reconnect()
            print('reconnected')

    def message(self, pubnub, message):
        print("({0}) {1}:    {2}".format(message.message["time"], message.message["nickname"], message.message["msg"]))

    def presence(self, pubnub, presence):
        pass

def init_chatroom(nickname):
    pnconfig = PNConfiguration()
    pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
    pnconfig.publish_key = pubkey
    pnconfig.subscribe_key = subkey
    pnconfig.uuid = nickname
    pubnub = PubNub(pnconfig)
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('mychatroom').with_presence().execute()
    return pubnub

def post_msg(pubnub, nickname, msg):
    pubnub.publish().channel('mychatroom').message({'nickname': nickname, 'msg': msg, 'time': str(datetime.datetime.now())}).sync()

def here_now_callback(result, status):
    if status.is_error():
        return
    for channel_data in result.channels:
        print("number of participants: %s" % channel_data.occupancy)
    for occupant in channel_data.occupants:
        print("uuid: %s" % (occupant.uuid))

def list_participants(pubnub):
    pubnub.here_now() \
        .channels('mychatroom') \
        .include_uuids(True) \
        .pn_async(here_now_callback)

######## MAIN #########
def main(argv):
    parser = argparse.ArgumentParser(prog='chatroom', usage='%(prog)s nickname')
    parser.add_argument("nickname", type=str, action='store', help="nickname")
    args = parser.parse_args()
    if args.nickname == "":
        usage()
        sys.exit()

    pubnub = init_chatroom(args.nickname)
    while True:
        msg = input()
        if msg == "list participants":
            list_participants(pubnub)
        else:
            post_msg(pubnub, args.nickname, msg)

if __name__ == "__main__":
    main(sys.argv[1:])
