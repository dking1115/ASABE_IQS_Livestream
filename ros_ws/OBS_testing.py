import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

ws = simpleobsws.WebSocketClient(url = 'ws://192.168.1.139:4455', password = 'ZDT4dGz7WYcbM5EY', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    #request = simpleobsws.Request('GetVersion') # Build a Request object
    #request = simpleobsws.Request('SetCurrentProgramScene') # Build a Request object
    #request.requestData={"sceneName":"Scene 2"}
    request = simpleobsws.Request('GetSceneList')
    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
        results=ret.responseData
        print(results["scenes"])
        for i in results["scenes"]:
            print(i["sceneName"])


    await ws.disconnect() # Disconnect from the websocket server cleanly

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())