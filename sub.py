from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
 
pnconfig = PNConfiguration()
 
pnconfig.publish_key = 'pub-c-c408ce7d-fe0d-4f9a-aae9-e67d5c9b6bd9'
pnconfig.subscribe_key = 'sub-c-efaf056a-75c7-11e9-b68a-fa5eae84dea0'
 
pubnub = PubNub(pnconfig)
 
my_listener = SubscribeListener()
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels('awesomeChannel').execute()
my_listener.wait_for_connect()
print('connected')
 
result = my_listener.wait_for_message_on('awesomeChannel')
print(result.message)
 
pubnub.unsubscribe().channels('awesomeChannel').execute()
my_listener.wait_for_disconnect()
 
print('unsubscribed')
exit(0)
