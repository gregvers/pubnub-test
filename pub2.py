from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

pnconfig = PNConfiguration()

pnconfig.publish_key = 'pub-c-c408ce7d-fe0d-4f9a-aae9-e67d5c9b6bd9'
pnconfig.subscribe_key = 'sub-c-efaf056a-75c7-11e9-b68a-fa5eae84dea0'

pubnub = PubNub(pnconfig)


class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).sync()

    def message(self, pubnub, message):
        print(message.message)

    def presence(self, pubnub, presence):
        pass


pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels("awesomeChannel").execute()
