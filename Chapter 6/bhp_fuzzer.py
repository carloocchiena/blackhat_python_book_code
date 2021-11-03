import random

from burp import IBurpExtender
from burp import IIintruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList


class BurpExtender(IBurpExtender, IIintruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    @staticmethod
    def getGeneratorName():
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        print("BHP Fuzzer initialized")
        self.max_payloads = 500 # book's data is 1000 here
        self.num_payloads = 0
    
        return

    def hasMorePayloads(self):
        print("hasMorePayloads called")
        if self.num_payloads == self.max_payloads:
            print("No more payloads")
            return False
        else:
            print("More payloads, continuing")
            return True
        
    def getNextPayload(self, current_payload):

        # convert the payload into a string
        payload = "".join(chr(x) for x in current_payload)

        # call our mutator to fuzz the post and increase the num of attempts
        payload = self.mutate_payload(payload)
        self.num_payloads += 1
        return payload

    def reset(self):
        self.num_payloads = 0
        return

    @staticmethod
    def mutatePayload(original_payload):
        picker = random.randint(1, 3)

        # select a random offset in the payload to mutate
        offset = random.randint(0, len(original_payload) - 1)
        payload = original_payload[:offset]

        # random offset insert a SQL injection attempt
        if picker == 1:
            payload += "'"

        # jam an XSS attempt in
        if picker == 2:
            payload += "<script>alert('BHP!');</script>"

        # repeat a chunk of the original payload a random number
        if picker == 3:
            chunk_length = random.randint(len(payload[offset:]), len(payload) - 1)
            repeater = random.randint(1, 10)
            for i in range(repeater):
                payload += original_payload[offset:offset + chunk_length]

        # add the remaining bits of the payload
        payload += original_payload[offset:]
        return payload
