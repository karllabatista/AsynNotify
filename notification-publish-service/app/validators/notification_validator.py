class NotificationValidator:
    VALID_CHANNELS = {"email", "sms", "push"}

    @staticmethod
    def validate(user_id:str,message:str,channel:str) ->bool:
      
        if not user_id or not message:
            return False
        if channel not in NotificationValidator.VALID_CHANNELS:
            return False
        return True