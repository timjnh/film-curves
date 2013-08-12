from ..annotation_plot_element import AnnotationPlotElement

class ZoneDevelopmentAnnotationPlotter(AnnotationPlotElement):
  def __init__(self, curve, **kws):
    AnnotationPlotElement.__init__(self, kws)
    self.curve = curve
    
  def get_text(self):
    return 'N{:+0.1f}'.format(self.curve.zone_development)
    
  def get_position(self):
    return self.curve.id_max_revised
