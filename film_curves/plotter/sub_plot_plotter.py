import matplotlib.pyplot as plt
from root_plot_element import RootPlotElement

class SubPlotPlotter(RootPlotElement):
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    RootPlotElement.__init__(self, [], {})
    
  def render(self):
    i = 0
    for element in self.elements:
      i += 1
      plt.subplot(self.rows, self.cols, i)
      element.render()