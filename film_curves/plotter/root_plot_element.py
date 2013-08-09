from plot_element import PlotElement
import matplotlib.pyplot as plt

class RootPlotElement(PlotElement):
  def __init__(self, valid_options, kws):
    PlotElement.__init__(self, valid_options, kws)
    
  def clear(self):
    plt.clf()