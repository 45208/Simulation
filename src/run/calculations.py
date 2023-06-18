from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
from ..board import Point

def scale_vector(vector: Point, dist: float):
    mult = (vector[0] ** 2 + vector[1] ** 2) ** 0.5 / dist
    if abs(mult) > 1e-9:
        vector = (vector[0] / mult, vector[1] / mult)
    return vector

# Reference: https://stackoverflow.com/questions/19394505/expand-the-line-with-specified-width-in-data-unit/42972469
class LineDataUnits(Line2D):
    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("lw", 1)
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data

    def _get_lw(self):
        if self.axes is not None:
            ppd = 72./self.axes.figure.dpi
            trans = self.axes.transData.transform
            return ((trans((1, self._lw_data))-trans((0, 0)))*ppd)[1]
        else:
            return 1

    def _set_lw(self, lw):
        self._lw_data = lw

    _linewidth = property(_get_lw, _set_lw)

def draw_spray_range(a: Point, b: Point, ax: plt.Axes, **kwargs):
    line = LineDataUnits([a[0], b[0]], [a[1], b[1]], **kwargs)
    ax.add_line(line)
