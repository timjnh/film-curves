import matplotlib.pyplot as plt

class PlotFigure(object):
  _figures = 0  
  
  def __init__(self, root_plot_element, **options):
    PlotFigure._figures += 1
    self.root_plot_element = root_plot_element
    self.options = options

  @staticmethod    
  def close_all():
    plt.close('all')
    
  def show(self):
    if PlotFigure._figures > 1:
      plt.figure()

    if 'name' in self.options:
      plt.gcf().canvas.set_window_title(self.options['name'])
      
    self.root_plot_element.render()
    self.root_plot_element.show()