class NotificationRequest:

    
    def __init__(self,user_id,message,channel):
        self.user_id = user_id
        self.message = message
        self.channel = channel

    def to_dict(self):

        return {
            "user_id" :self.user_id,
            "message": self.message,
            "channel":self.channel
        }
