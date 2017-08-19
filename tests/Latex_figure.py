import os
import numpy as np
import matplotlib as mpl
mpl.use('pgf')

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from Core.utils import check_dir


class LatexFigure:
    FOLDER_RESULTS = 'latex_images' + os.path.sep

    def __init__(self, width):
        size = LatexFigure.figsize(width)
        size[1] = size[1]/2
        plt.clf()
        self.fig = plt.figure(figsize=size) # matplotlib.figure.Figure instance
        self.ax = self.fig.add_subplot(111) # matplotlib.axes.Axes instance

    def plot(self, graphic, xlabel, ylabel):
        self.ax.plot(graphic)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plotNorm(self, data, nameData, title, placeLegend = False):
        self.distNorm(data, nameData)
        self.ax.set_xlabel('Values')
        self.ax.set_ylabel('Probability')
        # self.ax.title = title

        self.ax.set_xlim([0, 255])
        self.ax.set_ylim([0, 0.175])
        if placeLegend:
            self.ax.legend()

    def distNorm(self, data, label):
        data = sorted(data)
        pdf = mlab.normpdf(data, np.mean(data), np.std(data))
        self.ax.plot(data, pdf, label=label)  # including h here is crucial
        self.ax.hist(data, bins=30, normed=True)  # use this to draw histogram of your data


    def save(self, filename):
        check_dir(self.FOLDER_RESULTS)
        filename = self.FOLDER_RESULTS + filename
        plt.savefig('{}.pgf'.format(filename))
        plt.savefig('{}.pdf'.format(filename))

    @staticmethod
    def figsize(scale):
        fig_width_pt = 469.755  # Get this from LaTeX using \the\textwidth
        inches_per_pt = 1.0 / 72.27  # Convert pt to inch
        golden_mean = (np.sqrt(5.0) - 1.0) / 2.0  # Aesthetic ratio (you could change this)
        fig_width = fig_width_pt * inches_per_pt * scale  # width in inches
        fig_height = fig_width * golden_mean  # height in inches
        fig_size = [fig_width, fig_height]
        return fig_size





pgf_with_latex = {  # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",  # change this if using xetex or lautex
    "text.usetex": True,  # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],  # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,  # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,  # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": LatexFigure.figsize(0.9),  # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",  # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",  # plots will be generated using this preamble
    ]
}
mpl.rcParams.update(pgf_with_latex)
