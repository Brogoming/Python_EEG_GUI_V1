from PyQt5 import QtWidgets, QtCore, uic
import pyqtgraph as pg
import logging
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, WindowOperations
import sys  # We need sys so that we can pass argv to QApplication
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, board_shim, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.barGraph = None
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate

        # Load the UI Page
        uic.loadUi('GUI_V1.ui', self)

        self._init_timeseries()  # initializes time series widget
        self._init_bandpower()  # initializes band power widget

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.update_speed_ms)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.graphWidget.addPlot(row=i, col=0)
            p.showAxis('left', True)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def _init_bandpower(self):
        y = [0, 0, 0, 0, 0]
        xLab = ['Delta', "Theta", 'Alpha', 'Beta', 'Gamma']
        self.xVal = list(range(len(xLab)))
        ticks = []
        for i, item in enumerate(xLab):
            ticks.append((self.xVal[i], item))
        ticks = [ticks]
        self.b = self.bandWidget.addPlot()
        self.b.setMouseEnabled(x=False, y=False)  # Disable mouse panning & zooming
        self.b.hideButtons()  # Disable corner auto-scale button
        xAxis = self.b.getAxis('bottom')
        xAxis.setTicks(ticks)  # sets the ticks for the x-axis
        yAxis = self.b.getAxis('left')
        yAxis.setLabel("Power -- (uV)^2 / Hz")  # sets the left side label
        self.b.setYRange(0, 100, padding=0)
        self.barGraph = pg.BarGraphItem(x=self.xVal, height=y, width=0.5, brush='r')
        self.b.addItem(self.barGraph)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        band_power_delta = 0
        band_power_theta = 0
        band_power_alpha = 0
        band_power_beta = 0
        band_power_gamma = 0
        for count, channel in enumerate(self.exg_channels):  # count(int) = loop number, channel(int) = eeg channel
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 3.0, 45.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            self.curves[count].setData(data[channel].tolist())
            psd = DataFilter.get_psd_welch(data[channel], nfft, nfft // 2, self.sampling_rate,
                                           WindowOperations.BLACKMAN_HARRIS.value)
            band_power_delta += DataFilter.get_band_power(psd, 0.5, 4)
            band_power_theta += DataFilter.get_band_power(psd, 4.01, 8)
            band_power_alpha += DataFilter.get_band_power(psd, 8.01, 13.0)
            band_power_beta += DataFilter.get_band_power(psd, 13.01, 30.0)
            band_power_gamma += DataFilter.get_band_power(psd, 30.01, 50)
        avg_delta = band_power_delta / len(self.exg_channels)
        avg_theta = band_power_theta / len(self.exg_channels)
        avg_alpha = band_power_alpha / len(self.exg_channels)
        avg_beta = band_power_beta / len(self.exg_channels)
        avg_gamma = band_power_gamma / len(self.exg_channels)
        self.update_bar_graph(avg_delta, avg_theta, avg_alpha, avg_beta, avg_gamma)
        QtWidgets.QApplication.processEvents()

    def update_bar_graph(self, band_power_delta, band_power_theta, band_power_alpha, band_power_beta,
                         band_power_gamma):
        self.b.removeItem(self.barGraph)  # gets rid of the old graph
        self.barGraph = pg.BarGraphItem(x=self.xVal,
                                        height=[band_power_delta, band_power_theta,
                                                band_power_alpha, band_power_beta, band_power_gamma],
                                        width=0.5, brushes=['r', 'y', 'g', 'b', 'm'])
        self.b.addItem(self.barGraph)  # adds new graph with new band power values


def main():
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    params = BrainFlowInputParams()
    params.serial_port = "COM3"
    board_id = BoardIds.CYTON_DAISY_BOARD.value

    board_shim = BoardShim(board_id, params)
    try:
        board_shim.prepare_session()
        board_shim.start_stream(450000)
        time.sleep(10)  # give it time to warm up
        app = QtWidgets.QApplication(sys.argv)
        app.setAttribute(QtCore.Qt.AA_Use96Dpi)  # need this to work with other screens
        main = MainWindow(board_shim)
        main.show()
        app.exec_()
    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()


if __name__ == '__main__':
    main()
