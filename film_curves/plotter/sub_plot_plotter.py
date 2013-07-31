import matplotlib.pyplot as plt
from plot_element import PlotElement

class SubPlotPlotter(PlotElement):
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.plotters = []
    
  def add_plotter(self, plotter):
    self.plotters.append(plotter)
    
  def render(self):
    i = 0
    for plotter in self.plotters:
      i += 1
      plt.subplot(self.rows, self.cols, i)
      plotter.render()
      
    
  