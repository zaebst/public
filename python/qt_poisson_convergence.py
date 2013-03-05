#!/usr/bin/python

"""
Thanks to:
  Eli Bendersky for information on embedding matplotlib graphs in Qt http://eli.thegreenplace.net/2009/01/20/matplotlib-with-pyqt-guis/
  James Battat for info on fitting distributions with scipy https://www.cfa.harvard.edu/~jbattat/computer/python/science/#fitPoly

"""
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import uncertainties
from uncertainties import ufloat

import math
from math import sqrt
from math import  pow
from math import exp

import numpy
import scipy
from scipy import optimize


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Convergence of Poisson distribution')

        self.create_menu()
        self.create_main_frame()

        self.on_draw()

    def on_about(self):
        msg = """  An example of how poisson distributions can be approximated, showing the convergence of the poission distribution.
        """
        QMessageBox.about(self, "About: ", msg.strip())

    def on_draw(self):
        pi =  ufloat((3.14159265, 0.00000005))
        mu = self.slider.value()
        neg_mu = -1 * mu
        x_coords = []
        y_coords = []
        p_0    = exp(neg_mu)
        p_last = 0
        '''The poisson distribution is approximated by recursion: P(n) = (mu)/n P(n-1) '''
        for point in (numpy.linspace(0, 60, 60)):
            if ( point == 0 ):
               x_coords.append(point)
               y_coords.append(p_0)
               p_last = p_0
            else:
               p_new = mu/point*p_last
               x_coords.append(point)
               y_coords.append(p_new)
               p_last = p_new


        ''' numpy info on gaussian fitting from https://www.cfa.harvard.edu/~jbattat/computer/python/science/#fitPoly '''
        fitfunc = lambda p, x: p[0]*scipy.exp(-(x-p[1])**2/(2.0*p[2]**2))
        errfunc = lambda p, x, y: fitfunc(p,x)-y
        p0 = scipy.c_[max(y_coords), scipy.where(y_coords==max(y_coords))[0], 5]
        p1, success = scipy.optimize.leastsq(errfunc, p0.copy()[0],args=(x_coords,y_coords))
        y_coords_gaussian = fitfunc(p1, x_coords)
        constant_gaussian_point = p1[0]
        #print "constant gaussian c" , constant_gaussian_point
        central_gaussian_point  = p1[1]
        #print "gaussian mean" , central_gaussian_point
        gaussian_sigma = p1[2]
        #print "gaussian variance" , gaussian_sigma
        y_variance = numpy.array(y_coords).var()
        y_variance_squared = math.pow(y_variance,2)
        difference_array = numpy.array(y_coords) - numpy.array(y_coords_gaussian)
        diff_squared = numpy.square(difference_array)
        sum_diff_squared = diff_squared.sum()
        chi_squared = sqrt(sum_diff_squared/y_variance_squared)
        #print "Chi ", chi_squared

        # clear the axes
        self.axes.clear()
        # Redraw
        self.axes.axis([0,60,-.10,0.30])
        self.axes.set_autoscale_on(False)
        self.axes.plot(x_coords, y_coords, 'k.')
        self.axes.plot(x_coords, y_coords_gaussian, 'r-')
        self.axes.plot(x_coords, difference_array, 'b.')

        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QWidget()

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)

        # Slider for mu values
        slider_label = QLabel('Mean for Poisson Approximation')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(3, 30)
        self.slider.setValue(3)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)

        #
        # Layout with box sizers
        #
        hbox = QHBoxLayout()

        for w in [slider_label, self.slider]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)


    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu, (quit_action,))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About the demo')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()