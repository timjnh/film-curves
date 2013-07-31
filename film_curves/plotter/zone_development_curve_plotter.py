from plot_element import PlotElement
import numpy as np
import matplotlib.pyplot as plt

class ZoneDevelopmentCurvePlotter(PlotElement):
  def __init__(self, curve_family, **kws):
    self.min_development_time = 3
    self.max_development_time = 25
    self.include_points = False
    PlotElement.__init__(self, ['min_development_time', 'max_development_time', 'include_points'], kws)
    self.curve_family = curve_family
    
  def render(self):
    x_range = np.linspace(self.min_development_time, self.max_development_time, 50)
    plt.plot(x_range, self.curve_family.zone_development_best_fit_poly(x_range), '-')    

    if self.include_points:
      x, y = zip(*[ (curve.time, curve.zone_development) for curve in self.curve_family.curves ])
      x = list(x)
      y = list(y)
      x.append(20)
      y.append(1)
      plt.plot(x, y, '.')    
      
    self._finalizeLookNFeel()
      
  def _finalizeLookNFeel(self):
    plt.grid(linestyle='-.', linewidth=1, color='grey') 
    plt.gca().set_xticks(np.arange(self.min_development_time, self.max_development_time, 1))
    plt.gca().set_yticks(np.arange(-3, 2, .3))
    
    plt.xlim((self.min_development_time, self.max_development_time))
    plt.ylim((-3, 2))
    
    plt.gca().invert_yaxis()
    plt.legend(loc='best')