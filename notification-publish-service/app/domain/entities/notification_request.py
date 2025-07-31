class NotificationRequest:
    channels = {"email","sms","push"}
    
    def __init__(self,user_id:str,message:str,channel:str):

        if not self.validate(user_id,message,channel):
            raise ValueError("Invalid data to Notification Request")
        self.user_id = user_id
        self.message = message
        self.channel = channel

    def to_dict(self):

        return {
            "user_id" :self.user_id,
            "message": self.message,
            "channel":self.channel
        }

    @staticmethod
    def validate(user_id:str,message:str,channel:str) ->bool:
      
        if not user_id or not message:
            return False
        if channel not in NotificationRequest.channels:
            return False
        return True