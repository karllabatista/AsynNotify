from src.domain.entitites.notification import Notification
import pytest
def test_create_notification_instance():
    
    # ARRANGE
    user_id ="test_user_0123"
    message = " This is a message test"
    channel = " email"
    destination =  "test@email.com"


    # ACT
    notification = Notification(user_id,message,channel,destination)

    # ASSERT

    assert isinstance(notification,Notification)

def test_create_notification_invalid_fields_raises_value_error():

    # ARRANGE
    message = " This is a message test"
    channel = " email"
    destination =  "test@email.com"

    # ACT+ASSERT

    with pytest.raises(ValueError,match="Invalid mandatory fields"):
        Notification("",message,channel,destination)
