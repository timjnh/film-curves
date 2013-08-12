from ..annotation_plot_element import AnnotationPlotElement

class SbrAnnotationPlotter(AnnotationPlotElement):
  def __init__(self, curve, **kws):
    AnnotationPlotElement.__init__(self, kws)
    self.curve = curve
  
  def get_position(self):
    return self.curve.id_max_revised
  
  def get_text(self):
    sbr_stops = self.curve.subject_brightness_range / .3
    return 'SBR {:0.1f} stops'.format(sbr_stops)