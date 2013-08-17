from ..plot_element import PlotElement
import matplotlib.pyplot as plt

class ZoneDevelopmentAnnotationPlotter(PlotElement):
  def __init__(self, **kws):
    PlotElement.__init__(self, [], kws)
    
  def render(self):
    for n in range(-2, 2):
      iso = self.curve_family.effective_film_speed_for_zone(n)
      plt.annotate('N{:+d}, ISO {:d}'.format(n, int(round(iso))),
                        xy=(iso, n),
                        xytext=(0, 50),
                        textcoords='offset points',
                        horizontalalignment='center',
                        arrowprops=dict(arrowstyle="->"),
                        bbox=dict(boxstyle="round", fc="0.8"))