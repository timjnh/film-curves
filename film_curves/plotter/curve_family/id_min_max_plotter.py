from ..plot_element import PlotElement
import numpy as np
import matplotlib.pyplot as plt

class IdMinMaxPlotter(PlotElement):
  def __init__(self, curve_family, **kws):
    self.include_revised = False
    PlotElement.__init__(self, ['include_revised'], kws)
    self.curve_family = curve_family
    
  def render(self):
    x_range = np.linspace(self.min_x_range, self.curve_family.calibration_scale.first, 50)
    plt.plot(x_range, self.curve_family.id_min_best_fit_poly(x_range), '--', label='ID Min', color='grey')
    plt.plot(x_range, self.curve_family.id_max_best_fit_poly(x_range), '--', label='ID Max', color='grey')
    
    if self.include_revised:
      plt.plot(x_range, self.curve_family.id_min_revised_best_fit_poly(x_range), '--', label='ID Min Revised', color='black')
      plt.plot(x_range, self.curve_family.id_max_revised_best_fit_poly(x_range), '--', label='ID Max Revised', color='black')