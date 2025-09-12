class EventBusError(Exception):
    """
    Generic Error of event bus
    """
    pass

class EventBusTemporaryError(EventBusError):
    """
    Temporary error, retry can be solve
    """
    pass

class EventBusPermanentError(EventBusError):
    """PermanentError,  retry does not solve"""
    pass

