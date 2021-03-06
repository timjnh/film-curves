from ..plot_element import PlotElement
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
    
    i = 0
    for curve in self.curve_family.curves:      
      effective_speed, point = self.curve_family.calc_effective_speed_and_point_for(curve)
      annotation_options = self.annotation_options.get(curve.name, {})
      annotation_options = dict(annotation_options.items() + { 'offset': (20 + ((self.curve_family.curve_count - i) * 30), 0) }.items())
      self._add_speed_annotation(effective_speed, point, **annotation_options)
      i += 1
    
  def _add_speed_annotation(self, text, point, **kws):
    position = 0, -50 - point[1]
    if 'offset' in kws:
      position = position[0] + kws['offset'][0], position[1] + kws['offset'][1]
      del kws['offset']
      
    options = { 'xy': point,
                'xytext': position,
                'textcoords': 'offset points',
                'horizontalalignment': 'center',
                'arrowprops': dict(arrowstyle="->"),
                'bbox': dict(boxstyle="round", fc="0.8") }
    plt.annotate(text, **dict(options.items() + kws.items()))