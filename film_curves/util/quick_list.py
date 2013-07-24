class QuickList(list):
  @property
  def first(self):
    return self.__getitem__(0)
    
  @property
  def last(self):
    return self.__getitem__(len(self) - 1)