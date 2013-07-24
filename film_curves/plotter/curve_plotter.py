from plot_element import PlotElement
import numpy as np
import matplotlib.pyplot as plt

class CurvePlotter(PlotElement):
  def __init__(self, curve, **kws):
    self.include_points = False
    PlotElement.__init__(self, ['include_points'], kws)
    self.curve = curve
    self.plot_options = kws
    
  def render(self):    
    min_range = self.curve.calibration_scale.last
    if self.min_x_range is not None:
      min_range = self.min_x_range
    
    x_range = np.linspace(min_range, self.curve.calibration_scale.first, 50)
    if self.include_points:
      point_options = dict(self.plot_options.items() + { 'label': '_nolegend_' }.items())
      plt.plot(self.curve.calibration_scale, self.curve.data, '.', **point_options)
    plt.plot(x_range, self.curve.best_fit_poly(x_range), '-', **self.plot_options)    