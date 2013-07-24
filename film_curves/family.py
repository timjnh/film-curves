from curve import Curve
import numpy as np
from util.cached_property import cached_property
from util.quick_list import QuickList

class Family(object):
  def __init__(self):
    self._ordered_curves = []
    self._curves = {}
    self._calibration_scale = []
  
  def add_curve(self, *args):
    if len(args) == 1:
      curve = args[0]
      curve.calibration_scale = self._calibration_scale
    else:
      curve = Curve(args[0], args[1], self._calibration_scale)
    self._ordered_curves.append(curve.name)
    self._curves[curve.name] = curve
    
  @property
  def calibration_scale(self):
    return self._calibration_scale
    
  @calibration_scale.setter
  def calibration_scale(self, value):
    self._calibration_scale = QuickList(value)
    for curve in self._curves.itervalues():
      curve.calibration_scale = value
    
  @property
  def curves(self):
    for curve_name in self._ordered_curves:
      yield self._curves[curve_name]
      
  @property
  def min_x_range(self):
    return min([ curve.id_max_revised[0] for curve in self.curves ])

  @cached_property
  def id_min_best_fit_poly(self):
    (x, y) = zip(*[ curve.id_min for curve in self.curves ])
    return np.poly1d(np.polyfit(x, y, 1))
  
  @cached_property
  def id_max_best_fit_poly(self):
    (x, y) = zip(*[ curve.id_max for curve in self.curves ])
    return np.poly1d(np.polyfit(x, y, 1))
    
  @cached_property
  def id_min_revised_best_fit_poly(self):
    (x, y) = zip(*[ curve.id_min_revised for curve in self.curves ])
    return np.poly1d(np.polyfit(x, y, 1))
  
  @cached_property  
  def id_max_revised_best_fit_poly(self):      
    (x, y) = zip(*[ curve.id_max_revised for curve in self.curves ])
    return np.poly1d(np.polyfit(x, y, 1))
    
  @property
  def max_density(self):
    return max([ curve.data.last for curve in self.curves ])
    
#  # sort out where the iso standard lies
#  iso_gradient = .8 / 1.3
#  min_gradient = max_gradient = None
#  sorted(iso_gradients, key=lambda gradient: gradient[1])
#  for gradient in iso_gradients:
#    print gradient
#    if min_gradient is None or (gradient[1] > min_gradient and gradient[1] < iso_gradient):
#      min_gradient = gradient
#    if max_gradient is None or (gradient[1] < max_gradient and gradient[1] > iso_gradient):
#      max_gradient = gradient