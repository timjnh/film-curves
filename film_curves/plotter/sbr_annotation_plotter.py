from plot_element import PlotElement
import matplotlib.pyplot as plt

class SbrAnnotationPlotter(PlotElement):
  def __init__(self, curve, **kws):
    self.offset_multiplier = 1
    PlotElement.__init__(self, ['offset_multiplier'], kws)
    self.curve = curve
  
  def render(self):
    sbr_stops = (self.curve.id_min_revised[0] - self.curve.id_max_revised[0]) / .3
    plt.annotate('SBR {:0.1f} stops'.format(sbr_stops),
                xy=self.curve.id_max_revised,
                xytext=(-50, 30 * self.offset_multiplier), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"),
                bbox=dict(boxstyle="round", fc="0.8"))