from app.use_cases.publish_notification import PublishNotificationUseCase
from unittest.mock import Mock
def test_publish_notification_successfully():

    #ARRANGE
    event ={
        "user_id":"123454",
        "message":"acho que ja vou deitar",
        "channel":"email"
    }
    event_bus_mock = Mock()
    #ACT
    use_case = PublishNotificationUseCase(event_bus_mock)
    use_case.execute(event)
    #ASSERT
    event_bus_mock.publish.assert_called_once_with(event)