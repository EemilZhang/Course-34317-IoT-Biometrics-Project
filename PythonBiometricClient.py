import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import sys
import os
#import logging
import time
import json
#import getopt
#from pandas import DataFrame

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Global Variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# host = input('Please enter your unique endpoint address: ')
host = "a2rcd1k48ok85g.iot.us-west-2.amazonaws.com"
#rootCA = input('Please enter the filepath of your Root CA credential file: ')
rootCA = "/Users/Eemil/Desktop/root_CA.crt"
AWSAccessKeyID = input('Please enter your AWS Access Key: ')
AWSSecretAccessKey = input('Please enter your AWS Secret Access Key: ')

os.environ['AWS_ACCESS_KEY_ID'] = AWSAccessKeyID 
os.environ['AWS_SECRET_ACCESS_KEY'] = AWSSecretAccessKey

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Logging Configure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#logger = None
#if sys.version_info[0] == 3:
#    logger = logging.getLogger("core")  # Python 3
#else:
#    logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
#logger.setLevel(logging.DEBUG)
#streamHandler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#streamHandler.setFormatter(formatter)
#logger.addHandler(streamHandler)

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Shadow Client Init ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Sets up the AWS IoT MQTT shadow client. 
myAWSIoTMQTTShadowClient = AWSIoTPyMQTT.AWSIoTMQTTShadowClient("testIoTPySDK",  useWebsocket=True)

# Configures the endpoint + credential.
myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
myAWSIoTMQTTShadowClient.configureCredentials(rootCA)

# Configures the auto-reconnect parameters.
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Shadow Client Init ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance
  

    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        print("Received a delta message:")
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        print(deltaMessage)
        print("Request to update the reported state...")
        newPayload = '{"state":{"desired":' "bpm"'}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        print("Sent.")
  
    def customShadowCallback_Update(self, payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")
        print("Request(s) successfully sent.")
        time.sleep(3)

  
      # Custom Shadow callback
      #
    def customShadowCallback_Get(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
           print("============================================")
           print("Latest reported diagnostic type (User/Request): ")
           payloadDict = json.loads(payload)
           deviceShadowState = json.dumps(payloadDict["state"]["reported"]["diagnostic"])
           print(deviceShadowState)
           
           print("Latest reported BPM:")
           payloadDict = json.loads(payload)
           deviceShadowState = json.dumps(payloadDict["state"]["reported"]["BPM"])
           print(deviceShadowState)
           
           print("Latest reported SPO2:")
           payloadDict = json.loads(payload)
           deviceShadowState = json.dumps(payloadDict["state"]["reported"]["SPO2"])
           print(deviceShadowState)
           print("============================================")
           time.sleep(3)

           
    def customShadowCallback_GetRequestCount(self, payload, responseStatus, token):
           print("Latest reported SPO2:")
           payloadDict = json.loads(payload)
           requestCount = json.dumps(payloadDict["state"]["desired"]["RequestDiagnostic"])
           return requestCount
           
    def customShadowCallback_GetPendingRequests(self, payload, responseStatus, token):
           print("============================================")
           print("Current request state (Request/No request): ")
           payloadDict = json.loads(payload)
           deviceRequestState = json.dumps(payloadDict["state"]["desired"]["diagnostic"])
           print(deviceRequestState)
           
           print("Current BPM request state (True/False): ")
           payloadDict = json.loads(payload)
           bpmRequestState = json.dumps(payloadDict["state"]["desired"]["BPM"])
           print(bpmRequestState)
           
           print("Current SPO2 request state (True/False): ")
           payloadDict = json.loads(payload)
           spo2RequestState = json.dumps(payloadDict["state"]["desired"]["SPO2"])
           print(spo2RequestState)
           print("============================================")
           time.sleep(3)

          

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
myDeviceShadow = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("Eemil", True)
shadowCallbackContainer_myDeviceShadow = shadowCallbackContainer(myDeviceShadow)

time.sleep(3)

# Gets current state of device shadow
#myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_Get,5)

# Listen on deltas
# myDeviceShadow.shadowRegisterDeltaCallback(shadowCallbackContainer_myDeviceShadow.customShadowCallback_Delta)

# Shadow operations
# myDeviceShadow.shadowGet(customCallback, 5)
# myDeviceShadow.shadowUpdate(myJSONPayload, customCallback, 5)
# myDeviceShadow.shadowDelete(customCallback, 5)
# myDeviceShadow.shadowRegisterDeltaCallback(customCallback)
# myDeviceShadow.shadowUnregisterDeltaCallback()

#loop
while True:
    print("")
    print("===========================================")
    print("Remote patient biometrics monitoring system")
    print("-------------------------------------------")
    print("")
    print("1. Request patient biometric reading.")
    print("2. View current pending requests")
    print("3. View latest patient biometric reading.")
    print("4. Quit")
    print("")
    print("===========================================")
    menuOption = '0'    
    while menuOption == '0':
        menu = input(">> Please input the number of the desired option: ")
        
        if menu == '1':
            print("------------------------")
            print("Diagnostics request menu")
            print("------------------------")
            print("")
            print("1. BPM.")
            print("2. SPO2.")
            print("3. Request all diagnostics.")
            print("4. Withdraw all requests.")
            print("")
            print("------------------------")
            diagnosticID = input(">> Please input the number of the diagnostic you would like to request: ")
            diagnosticLoop = '0'
            while diagnosticLoop == '0':
                if diagnosticID == '1':     
                    JSONPayload = '{"state":{"desired":{"diagnostic":"Request"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"BPM": "True"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"SPO2": "False"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    #requestCount = myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_GetRequestCount,5)
                    #requestCount = str(requestCount + 1)
                    #JSONPayload = '{"state":{"desired":{"RequestDiagnostic":' + str(requestCount) + '}}}'
                    #myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    diagnosticLoop = '1'
                elif diagnosticID == '2':
                    JSONPayload = '{"state":{"desired":{"diagnostic":"Request"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"BPM":"False"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"SPO2":"True"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    #requestCount = myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_GetRequestCount,5)
                    #requestCount = str(requestCount + 1)
                    #JSONPayload = '{"state":{"desired":{"RequestDiagnostic":' + str(requestCount) + '}}}'
                    #myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    diagnosticLoop = '2'

                elif diagnosticID == '3':
                    JSONPayload = '{"state":{"desired":{"diagnostic":"Request"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"BPM":"True"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"SPO2":"True"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    #requestCount = myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_GetRequestCount,5)
                    #requestCount = str(requestCount + 1)
                    #JSONPayload = '{"state":{"desired":{"RequestDiagnostic":' + str(requestCount) + '}}}'
                    #myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    diagnosticLoop = '3'
                
                elif diagnosticID == '4':
                    JSONPayload = '{"state":{"desired":{"diagnostic":"No request"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"BPM":"False"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    JSONPayload = '{"state":{"desired":{"SPO2":"False"}}}'
                    myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    #requestCount = myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_GetRequestCount,5)
                    #requestCount = str(requestCount + 1)
                    #JSONPayload = '{"state":{"desired":{"RequestDiagnostic":' + str(requestCount) + '}}}'
                    #myDeviceShadow.shadowUpdate(JSONPayload,shadowCallbackContainer_myDeviceShadow.customShadowCallback_Update, 5)
                    diagnosticLoop = '4'
                    

                else:
                    print('"Error": This is not a valid option, please input the number of the desired option: ')
                    diagnosticLoop == '0'
            
            menuOption = '1'
        
        elif menu == '2':
            myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_GetPendingRequests,5)
            time.sleep(1)
            menuOption = '2'
            
        elif menu == '3':
            myDeviceShadow.shadowGet(shadowCallbackContainer_myDeviceShadow.customShadowCallback_Get, 5)
            time.sleep(1)
            menuOption = '3'     
        
        elif menu == '4':
            sys.exit()
        
        else:
            print('"Error": This is not a valid option, please input the number of the desired option: ')
            
    pass