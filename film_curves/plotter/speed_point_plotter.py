from plot_element import PlotElement
import numpy as np
import matplotlib.pyplot as plt

class SpeedPointPlotter(PlotElement):
  def __init__(self, curve_family, **kws):
    self.annotation_options = {}
    PlotElement.__init__(self, ['annotation_options'], kws)
    self.curve_family = curve_family
    
  def render(self):
    x_range = np.linspace(self.curve_family.speed_point[0], self.curve_family.speed_point[0] - 1.3, 50)
    plt.plot(x_range, self.curve_family.iso_gradient_best_fit_poly(x_range), '--', label='Speed Point Gradient', color='black')
    
    self._add_speed_annotation(self.curve_family.iso_speed, self.curve_family.speed_point)
    
    for curve in self.curve_family.curves:
      effective_speed = curve.calc_effective_speed(self.curve_family.speed_point, self.curve_family.iso_speed)
      annotation_options = self.annotation_options.get(curve.name, {})
      self._add_speed_annotation(effective_speed, curve.id_min, **annotation_options)
    
  def _add_speed_annotation(self, text, point, **kws):
    options = { 'xy': point,
                'xytext': (0, -50 - point[1]),
                'textcoords': 'offset points',
                'horizontalalignment': 'center',
                'arrowprops': dict(arrowstyle="->"),
                'bbox': dict(boxstyle="round", fc="0.8") }
    plt.annotate(text, **dict(options.items() + kws.items()))