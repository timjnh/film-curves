import film_curves as fc

step_tablet = [2.99, 2.84, 2.71, 2.56, 2.44, 2.31, 2.19, 2.04, 1.89, 1.74, 1.57, 1.43, 1.27, 1.12, 0.98, 0.83, 0.66, 0.53, 0.36, 0.2, 0.06, 0]

ordered_configurations = ['four_minutes', 'five_and_a_half_minutes', 'eight_minutes', 'eleven_minutes', 'sixteen_minutes']
plot_configuration = {
  'four_minutes': {
    'data': [0.05, 0.06, 0.06, 0.06, 0.08, 0.09, 0.12, 0.15, 0.19, 0.24, 0.3, 0.35, 0.38, 0.45, 0.51, 0.56, 0.62, 0.69, 0.74, 0.81, 0.88, 0.97],
    'plot_options': { 'color': 'red', 'label': '4 Minutes' }
  },
  'five_and_a_half_minutes': {
    'data': [0.06, 0.06, 0.07, 0.08, 0.11, 0.14, 0.17, 0.21, 0.26, 0.34, 0.41, 0.48, 0.55, 0.63, 0.71, 0.78, 0.85, 0.94, 1, 1.09, 1.17, 1.26],
    'plot_options': { 'color': 'orange', 'label': '5:30 Minutes' }
  },
  'eight_minutes': {
    'data': [0.06, 0.07, 0.09, 0.11, 0.14, 0.18, 0.22, 0.27, 0.34, 0.42, 0.5, 0.59, 0.69, 0.79, 0.88, 0.97, 1.05, 1.15, 1.24, 1.34, 1.43, 1.53],
    'plot_options': { 'color': 'yellow', 'label': '8 Minutes' }
  },
  'eleven_minutes': {
    'data': [0.08, 0.08, 0.1, 0.13, 0.17, 0.22, 0.28, 0.35, 0.44, 0.54, 0.65, 0.76, 0.84, 0.96, 1.06, 1.17, 1.27, 1.38, 1.47, 1.57, 1.68, 1.78],
    'plot_options': { 'color': 'green', 'label': '11 Minutes' }
  },
  'sixteen_minutes': {
    'data': [0.08, 0.11, 0.13, 0.16, 0.2, 0.26, 0.34, 0.42, 0.54, 0.68, 0.8, 0.93, 1.05, 1.2, 1.33, 1.45, 1.56, 1.7, 1.79, 1.92, 2.04, 2.15],
    'plot_options': { 'color': 'blue', 'label': '16 Minutes' }
  }
}

curve_family = fc.Family()

curve_family.calibration_scale = step_tablet
for k in ordered_configurations:
  curve_family.add_curve(k, plot_configuration[k]['data'])
  
i = 0
plotter = fc.plotter.Plotter()
for curve in curve_family.curves:
  i += 1
  
  plot_options = dict(plot_configuration[curve.name]['plot_options'].items() + { 'include_points': True }.items())
  plotter.add(fc.plotter.CurvePlotter(curve, **plot_options))
  plotter.add(fc.plotter.SbrPlotter(curve, offset_multiplier=6 - i))
  
plotter.add(fc.plotter.IdMinMaxPlotter(curve_family, include_revised=True))  
  
plotter.scale_for(curve_family)
plotter.render()