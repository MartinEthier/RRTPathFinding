# Original code from:
# https://stackoverflow.com/questions/40126176/fast-live-plotting-in-matplotlib-pyplot

import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.iteration_label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.iteration_label)

        self.canvas = pg.PlotWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.FPS_label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.FPS_label)

        #  line plot
        self.plot = self.canvas.addPlot()
        self.h2 = self.plot.plot(pen='y')

        #### Set Data  #####################

        self.x = np.linspace(0,50., num=100)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):

        self.ydata = np.sin(self.x/3.+ self.counter/9.)

        self.h2.setData(self.ydata)

        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate: {fps:.3f} FPS'.format(fps=self.fps )
        self.FPS_label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.iteration_label.setText("Iteration: {count}".format(count=self.counter))
        self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())