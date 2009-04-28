class Event:
  def __init__(self, x = None, y = None, b = None, key = None, character = None, wheelDelta = None):
    self.x = x
    self.y = y
    self.b = b
    self.key = key
    self.character = character
    self.wheelDelta = wheelDelta
    
  def __repr__(self):
    return "event: %s, %s, %s, %s, %s, " %(self.x, self.y, self.b, self.key, self.character)
    
class EventHandler:
  def __init__(self):
    pass
    
  def callEvent(self, eventType, event):
    if hasattr(self, eventType):
      getattr(self, eventType)(event)
      
  def attachEvent(self, eventName, eventMethod):
    setattr(self, eventName, eventMethod)
    
  def detachEvent(self, eventName):
    delattr(self, eventName)
      
  def event(self, eventMethod):
    self.attachEvent(eventMethod.__name__, eventMethod)