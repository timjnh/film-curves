from curve import Curve
import numpy as np
from scipy import optimize
from util import cached_property
from util import QuickList
from util import Poly
import math

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
      curve = Curve(args[0], args[1], args[2], self._calibration_scale)
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
  def curve_count(self):
    return len(self._curves)      
      
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
    
  def calc_effective_speed_and_point_for(self, curve, round_speed=True):
    intercept = curve.intercept(self.id_min_revised_best_fit_poly)
    
    third_stops_off = (self.speed_point[0] - intercept[0]) / .1
    iso_index = self.iso_film_speeds.index(self.iso_speed)
    
    if round_speed:
      return self.iso_film_speeds[iso_index + int(round(third_stops_off))], intercept
    else:
      max_speed = self.iso_film_speeds[iso_index + int(math.floor(third_stops_off))]
      min_speed = self.iso_film_speeds[iso_index + int(math.ceil(third_stops_off))]
      
      offset = ((max_speed - min_speed) * math.modf(third_stops_off)[0])
      if third_stops_off < 0:
        speed = min_speed - offset
      else:
        speed = max_speed - offset
      return speed, intercept

  def calc_effective_speed_for(self, curve, **kws):
    speed, speed_point = self.calc_effective_speed_and_point_for(curve, **kws)
    return speed

  @cached_property    
  def extended_film_speed_range(self):
    return self._film_speed_range(extension=4)
    
  def _film_speed_range(self, extension=0):
    curve_speed_indices = [ self.iso_film_speeds.index(self.calc_effective_speed_for(curve)) for curve in self.curves ]
    
    max_speed_index = max(curve_speed_indices) + extension
    min_speed_index = min(curve_speed_indices) - extension
    if max_speed_index >= len(self.iso_film_speeds):
      min_speed_index -= max_speed_index - (len(self.iso_film_speeds) - 1)
      max_speed_index = len(self.iso_film_speeds) - 1
    if min_speed_index < 0:     
      max_speed_index += 0 - min_speed_index
      min_speed_index = 0
    max_speed_index = min(max_speed_index, len(self.iso_film_speeds) - 1)
    
    speed_range = self.iso_film_speeds[min_speed_index:max_speed_index + 1]
    speed_range.reverse()
    return speed_range
    
  @cached_property
  def zone_film_speed_best_fit_poly(self):
    x = [ self.calc_effective_speed_for(curve, round_speed=False) for curve in self.curves ]
    y = [ curve.zone_development for curve in self.curves ]
    return np.poly1d(np.polyfit(x, y, 1))
    
  def effective_film_speed_for_zone(self, zone):
    return Poly.find_root_in_range(self.zone_film_speed_best_fit_poly - zone, (self.iso_film_speeds[-1], self.iso_film_speeds[0]))
    
  def _exponential_function(self, x, a, b, c):
    return (b * (a ** x)) + c
    
  @cached_property
  def zone_development_best_fit_poly(self):    
    x, y = zip(*[ (curve.time, curve.zone_development) for curve in self.curves ])
    
    popt, pcov = optimize.curve_fit(self._exponential_function, x, y, p0 = [1, 1, 1])
    def best_fit(x):
      return self._exponential_function(x, *popt)
    return best_fit
    
  def development_time_for_zone(self, n):
    def y_offset(x):
      return self.zone_development_best_fit_poly(x) - n
    return optimize.newton(y_offset, 0)