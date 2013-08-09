import numpy as np
import matplotlib.pyplot as plt
from plot_element import PlotElement

class CurveFamilyPlotter(PlotElement):
  def __init__(self):
    self.elements = []
    self._min_x_range = None
    
  def add(self, element):
    if self._min_x_range is not None:
      element.min_x_range = self._min_x_range
    self.elements.append(element)
  
  def render(self):
    for element in self.elements:
      element.render()
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