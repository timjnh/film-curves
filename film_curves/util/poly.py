class Poly(object):
  
  @staticmethod
  def intercept(poly1, poly2, root_range):
    x = Poly.find_root_in_range(poly1 - poly2, root_range, fuzzy_min=True)
    return x, poly1(x)
   
  @staticmethod
  def find_root_in_range(poly, root_range, fuzzy_min=False):
    root_in_range = None
    largest_root_below_range = None
    
    sorted_roots = poly.r
    sorted_roots.sort()
    
    for root in sorted_roots:
      if root < root_range[0] and (largest_root_below_range is None or root > largest_root_below_range):
        largest_root_below_range = root
      if root > root_range[0] and root < root_range[1]:
        root_in_range = root
        break
    if root_in_range is None:
      if fuzzy_min is True and largest_root_below_range is not None:
        return largest_root_below_range
      raise StandardError('Could not find valid root!')
    return root_in_range