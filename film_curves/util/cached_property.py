class cached_property(property):
  'Convert a method into a cached attribute'
  def __init__(self, method):
    private = '_' + method.__name__
    
    def fget(s):
      try:
        return getattr(s, private)
      except AttributeError:
        value = method(s)
        setattr(s, private, value)
        return value

    def fdel(s):
      del s.__dict__[private]
      super(cached_property, self).__init__(fget, fdel=fdel)
    
    property.__init__(self, fget, None, fdel)
   
  @staticmethod
  def reset(self):
    cls = self.__class__
    for name in dir(cls):
      attr = getattr(cls, name)
      if isinstance(attr, cached_property):
        delattr(self, name)