class Notification:

    def __init__(self,user_id:str,
                 message:str,
                 channel:str,
                 destination:str):
        
        if not self._validate(user_id,message,channel,destination):
            raise ValueError("Invalid mandatory fields")
        
        self.user_id = user_id 
        self.message = message
        self.channel = channel
        self.destination = destination


    @staticmethod
    def _validate(user_id:str,
                 message:str,
                 channel:str,
                 destination:str)->bool:

        return all([user_id,message,channel,destination])
    




