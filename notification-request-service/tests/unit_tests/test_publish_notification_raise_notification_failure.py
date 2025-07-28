from unittest.mock import Mock
from app.use_cases.publish_notification import PublishNotificationUseCase
from app.domain.exceptions.notification_publish_error import NotificationPublishError
import pytest

def test_publish_notifcation_failure():

    #ARRANGE
    event ={
        "user_id":"123454",
        "message":"acho que ja vou deitar",
        "channel":"email"
    }
    event_bus_mock = Mock()

    event_bus_mock.publish.side_effect = Exception()
    
    use_case = PublishNotificationUseCase(event_bus_mock)

    # act
    with pytest.raises(NotificationPublishError) as error_info:
        use_case.execute(event)

    assert str(error_info.value) == "Failed to publish event"