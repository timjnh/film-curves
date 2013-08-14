from plot_element import PlotElement
import matplotlib.pyplot as plt

class RootPlotElement(PlotElement):
  def __init__(self, valid_options, kws):
    self._elements = []
    PlotElement.__init__(self, valid_options, kws)
    
  @property
  def elements(self):
    return self._elements    
    
  def add(self, element):
    self._elements.append(element)    
    
  def clear(self):
    plt.clf()
    
  def render(self):
    for element in self._elements:
      element.render()