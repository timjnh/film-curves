from ..root_plot_element import RootPlotElement
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

class ZoneFilmSpeedCurvePlotter(RootPlotElement):
  def __init__(self, curve_family, **kws):
    self.include_points = False
    RootPlotElement.__init__(self, ['include_points'], kws)
    self.curve_family = curve_family
    
  def add(self, element):
    element.curve_family = self.curve_family
    RootPlotElement.add(self, element)    
    
  def render(self):
    plt.plot(self.curve_family.extended_film_speed_range, self.curve_family.zone_film_speed_best_fit_poly(self.curve_family.extended_film_speed_range), '-', color='blue')

    if self.include_points:
      x, y = zip(*[ (self.curve_family.calc_effective_speed_for(curve, round_speed=False), curve.zone_development) for curve in self.curve_family.curves ])
      plt.plot(x, y, '.', color='blue')
      
    RootPlotElement.render(self)
    self._finalize_look_n_feel()
      
      
  def _finalize_look_n_feel(self):
    plt.grid(linestyle='-.', linewidth=1, color='grey') 
    plt.gca().set_xticks(self.curve_family.extended_film_speed_range)
    plt.gca().set_yticks(np.arange(-3, 2, .3))
    
    plt.gca().get_yaxis().set_major_formatter(ticker.FormatStrFormatter('N%+0.1f'))
    
    plt.xlim((self.curve_family.extended_film_speed_range[0], self.curve_family.extended_film_speed_range[-1]))
    plt.ylim((-3, 2))
    
    plt.gca().invert_yaxis()
    plt.legend(loc='best')