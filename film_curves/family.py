from curve import Curve
import numpy as np
from util.cached_property import cached_property
from util.quick_list import QuickList

class Family(object):
  def __init__(self, iso_speed):
    self._ordered_curves = []
    self._curves = {}
    self._calibration_scale = []
    
    self.iso_gradient = .8 / 1.3
    self.iso_speed = iso_speed
    
    self.iso_film_speeds = [1600, 1300, 1000, 800, 650, 500, 400, 320, 250, 200, 160, 125, 100, 80, 64, 50, 40, 32, 25, 20, 16, 12, 10]
  
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
      
  def curve(self, name):
    return self._curves[name]      
      
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
    
  @cached_property
  def iso_gradient_best_fit_poly(self):
    iso_offset_speed_point = self.speed_point[0] - 1.3, self.speed_point[1] + .8
    x, y = zip(iso_offset_speed_point, self.speed_point)
    return np.poly1d(np.polyfit(x, y, 1))    
    
  @cached_property
  def speed_point(self):
    min_gradient, max_gradient = self._find_min_max_gradient_curves()
    gradient_ratio = (max_gradient[1] - self.iso_gradient) / (max_gradient[1] - min_gradient[1])
    
    min_gradient_id_min = self.curve(min_gradient[0]).id_min
    max_gradient_id_min = self.curve(max_gradient[0]).id_min
    
    offset_x = (max_gradient_id_min[0] - min_gradient_id_min[0]) * gradient_ratio
    offset_y = (max_gradient_id_min[1] - min_gradient_id_min[1]) * gradient_ratio
    
    return (max_gradient_id_min[0] - offset_x), (max_gradient_id_min[1] - offset_y)
    
    
  def _find_min_max_gradient_curves(self):
    min_gradient = max_gradient = None
    
    iso_gradients = [(curve.name, curve.iso_gradient) for curve in self.curves]
    for gradient in iso_gradients:
      if gradient[1] < self.iso_gradient and (min_gradient is None or gradient[1] > min_gradient[1]):
        min_gradient = gradient
      if gradient[1] > self.iso_gradient and (max_gradient is None or gradient[1] < max_gradient[1]):
        max_gradient = gradient
        
    if min_gradient is None:
      raise StandardError("No gradient was less than the ISO standard!  You probably need to change your development times")
    if max_gradient is None:
      raise StandardError("No gradient was greater than the ISO standard!  You probably need to change your development times")
      
    return min_gradient, max_gradient 
    
  def calc_effective_speed_and_point_for(self, curve):
    intercept = curve.intercept(self.id_min_revised_best_fit_poly)
    
    third_stops_off = round((self.speed_point[0] - intercept[0]) / .1)
    iso_index = self.iso_film_speeds.index(self.iso_speed)
    return self.iso_film_speeds[iso_index + int(third_stops_off)], intercept