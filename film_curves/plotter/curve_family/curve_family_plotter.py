import numpy as np
import matplotlib.pyplot as plt
from ..root_plot_element import RootPlotElement

class CurveFamilyPlotter(RootPlotElement):
  def __init__(self):
    self._min_x_range = None
    RootPlotElement.__init__(self, [], {})
    
  def add(self, element):
    if self._min_x_range is not None:
      element.min_x_range = self._min_x_range
    RootPlotElement.add(self, element)
  
  def render(self):
    RootPlotElement.render(self)
    self._finalize_look_n_feel()
    
  def _finalize_look_n_feel(self):
    plt.grid(linestyle='-.', linewidth=1, color='grey')    
    plt.gca().invert_xaxis()
    plt.legend(loc='best')

  def scale_for(self, curve_family):
    self.min_x_range = curve_family.min_x_range - .1
    
    plt.gca().set_xticks(np.arange(0, curve_family.calibration_scale.first + .1, .3))
    plt.gca().set_yticks(np.arange(0, curve_family.max_density + .1, .3))
    plt.xlim((curve_family.min_x_range, curve_family.calibration_scale.first + .1))
    plt.ylim((0, curve_family.max_density + 1))
      
  @property
  def min_x_range(self):
    return self._min_x_range
    
  @min_x_range.setter
  def min_x_range(self, value):
    self._min_x_range = value
    for element in self.elements:
      element.min_x_range = self._min_x_range