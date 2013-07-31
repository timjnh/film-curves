import matplotlib.pyplot as plt

class PlotElement(object):
  def __init__(self, valid_options, kws):
    self.min_x_range = None
    self._extract_options(valid_options, kws)
  
  def _extract_options(self, valid_options, options):
    for option in valid_options:
      if option in options:
        self.__setattr__(option, options[option])
        del options[option]
  
  def render(self):
    raise NotImplementedError("The base class PlotElement does not implement render")
    
  def show(self):
    plt.show();