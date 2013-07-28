from util.quick_list import QuickList
from util.cached_property import cached_property
import numpy as np

class Curve(object):
  def __init__(self, name, data, calibration_scale):
    self.name = name
    self.data = data
    self.calibration_scale = calibration_scale
    
  @property
  def data(self):
    return self._data
    
  @data.setter
  def data(self, value):
    self._data = QuickList(value)
    
  @property
  def calibration_scale(self):
    return self._calibration_scale
    
  @calibration_scale.setter
  def calibration_scale(self, value):
    self._calibration_scale = QuickList(value)
    
  @cached_property
  def best_fit_poly(self):
    return np.poly1d(np.polyfit(self.calibration_scale, self.data, 3))
    
  @property
  def id_min(self):
    return self._calc_id_min()
  
  def _calc_id_min(self, density_over_base_plus_fog=.1):
    id_min_y = self.data[0] + density_over_base_plus_fog
    id_min_x = self._find_root_in_range(self.best_fit_poly - id_min_y)
    return (id_min_x, id_min_y)
    
  @property
  def id_max(self):
    return self._calc_id_max(self.id_min[1])
    
  def _calc_id_max(self, id_min_y):
    id_max_y = id_min_y + 1.16
    id_max_x = self._find_root_in_range(self.best_fit_poly - id_max_y, fuzzy_min=True)
    return (id_max_x, id_max_y)

  @property
  def avg_gradient(self):
    return (self.id_max[1] - self.id_min[1]) / (self.id_min[0] - self.id_max[0])
    
  @property
  def id_min_revised(self):
    return self._calc_id_min(density_over_base_plus_fog=self.avg_gradient / 8.5)
    
  @property
  def id_max_revised(self):
    return self._calc_id_max(self.id_min_revised[1])
    
  def intercept(self, poly):
    x = self._find_root_in_range(self.best_fit_poly - poly, fuzzy_min=True)
    return x, self.best_fit_poly(x)
    
  def _find_root_in_range(self, poly, fuzzy_min=False):
    root_in_range = None
    largest_root_below_range = None
    
    sorted_roots = poly.r
    sorted_roots.sort()
    
    for root in sorted_roots:
      if root < self.calibration_scale.last and (largest_root_below_range is None or root > largest_root_below_range):
        largest_root_below_range = root
      if root > self.calibration_scale.last and root < self.calibration_scale.first:
        root_in_range = root
        break
    if root_in_range is None:
      if fuzzy_min is True and largest_root_below_range is not None:
        return largest_root_below_range
      raise StandardError('Could not find valid root!')
    return root_in_range    
    
  @property
  # Defining the iso_gradient as the slope that covers a vertical rise of .8 from id_min
  # Note that we switch the direction of the slope to give ourselvesa positive value
  def iso_gradient(self):
    slope_point_y = self.id_min[1] + .8
    slope_point_x = self._find_root_in_range(self.best_fit_poly - slope_point_y, fuzzy_min=True)
    slope_point = (slope_point_x, slope_point_y)
    return (slope_point[1] - self.id_min[1]) / (self.id_min[0] - slope_point[0])  
    
  @property
  def subject_brightness_range(self):
    return self.id_min_revised[0] - self.id_max_revised[0]
    
  @property
  def zone_development(self):
    zone_length = self.subject_brightness_range / 7.0
    return (1.2 - (zone_length * 4)) / .3