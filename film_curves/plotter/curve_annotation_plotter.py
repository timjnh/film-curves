from annotation_plot_element import AnnotationPlotElement
from sbr_annotation_plotter import SbrAnnotationPlotter
from zone_development_annotation_plotter import ZoneDevelopmentAnnotationPlotter

class CurveAnnotationPlotter(AnnotationPlotElement):
  def __init__(self, curve, **kws):
    AnnotationPlotElement.__init__(self, kws)
    self.curve = curve
    
    self.sbr_annotation_plotter = SbrAnnotationPlotter(self.curve, **kws)
    self.zone_development_annotation_plotter = ZoneDevelopmentAnnotationPlotter(self.curve)
    
  def get_position(self):
    return self.sbr_annotation_plotter.get_position()

  def get_text(self):
    return self.curve.name + "\n" + self.sbr_annotation_plotter.get_text() + "\n" + self.zone_development_annotation_plotter.get_text()
    
  @property
  def x_offset(self):
    return -55  
    
  @property
  def y_offset(self):
    return 50