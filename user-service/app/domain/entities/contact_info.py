class ContactInfo:

    def __init__(self,email:str,sms:str,prefered_channel:str ):
        self.email = email
        self.sms = sms
        self.prefered_channel=prefered_channel
  
    def to_dict(self):

        return {
            "email":self.email,
            "sms":self.sms,
            "prefered_channel":self.prefered_channel
        }