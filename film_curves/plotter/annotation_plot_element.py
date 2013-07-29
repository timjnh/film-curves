from plot_element import PlotElement
import matplotlib.pyplot as plt

class AnnotationPlotElement(PlotElement):
  def __init__(self, kws):
    self.offset_multiplier = 1
    PlotElement.__init__(self, ['offset_multiplier'], kws)
    
  def get_position(self):
    raise NotImplemented("The get_position method is abstract in AnnotationPlotElement")
  
  def get_text(self):
    raise NotImplemented("The get_text method is abstract in AnnotationPlotElement")
    
  @property
  def x_offset(self):
    return -50
    
  @property
  def y_offset(self):
    return 30
    
  def render(self):
    plt.annotate(self.get_text(),
                        xy=self.get_position(),
                        xytext=(self.x_offset, self.y_offset * self.offset_multiplier),
                        textcoords='offset points',
                        horizontalalignment='center',
                        arrowprops=dict(arrowstyle="->"),
                        bbox=dict(boxstyle="round", fc="0.8"))