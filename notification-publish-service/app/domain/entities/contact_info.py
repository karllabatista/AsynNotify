class ContactInfo:
    def __init__(self,email:str,sms:str,preferred_channel:str):

        if not self._validate(email,sms,preferred_channel):
            raise ValueError("Mandatory fields invalid")

        
        self.email = email
        self.sms =sms
        self.preferred_channel = preferred_channel

    
    @staticmethod
    def _validate(email:str,sms:str,preferred_channel:str) ->bool:
        
       return all([email,sms,preferred_channel])