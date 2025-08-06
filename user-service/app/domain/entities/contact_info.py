class ContactInfo:

    def __init__(self,email:str,sms:str,preferred_channel:str ):
        self.email = email
        self.sms = sms
        self.preferred_channel=preferred_channel
  
    def to_dict(self):

        return {
            "email":self.email,
            "sms":self.sms,
            "preferred_channel":self.preferred_channel
        }