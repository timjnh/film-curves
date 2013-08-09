from plot_element import PlotElement
import matplotlib.pyplot as plt

class ZoneDevelopmentCurveAnnotationPlotter(PlotElement):
  def __init__(self, **kws):
    PlotElement.__init__(self, [], kws)
    
  def render(self):
    for n in range(-2, 2):
      minutes = self.curve_family.development_time_for_zone(n)
      plt.annotate('N{:+d}, {:d} minutes'.format(n, int(round(minutes))),
                        xy=(minutes, n),
                        xytext=(0, 50),
                        textcoords='offset points',
                        horizontalalignment='center',
                        arrowprops=dict(arrowstyle="->"),
                        bbox=dict(boxstyle="round", fc="0.8"))