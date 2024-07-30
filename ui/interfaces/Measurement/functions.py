import serial
import struct
from PyQt5.QtCore import QThread, pyqtSignal
from colour import SpectralDistribution, sd_to_XYZ, XYZ_to_xyY, SDS_ILLUMINANTS, MSDS_CMFS, SpectralShape
import config

class MeasurementFunctions:
    def __init__(self, measurement_layout):
        self.measurement_layout = measurement_layout

    def start_listening(self):
        self.measurement_layout.label.setText("Listening to measurement...")
        self.measurement_layout.label_state = 0
        self.measurement_layout.timer.start(500)

        self.worker = SerialWorker()
        self.worker.data_received.connect(self.handle_data)
        self.worker.start()

    def handle_data(self, values):
        if values:
            self.measurement_layout.measurement_counter += 1
            self.measurement_layout.measurements.append(values)
            self.add_measurement_to_sample(f"Measurement {self.measurement_layout.measurement_counter}", values)
            self.stop_listening()

    def add_measurement_to_sample(self, name, values):
        x, y, Y = self.convert_to_xyY(values)
        sample_id = self.measurement_layout.measurement_counter
        config.measurement.append((sample_id, name, values))

        # Add the sample field with draggable widget
        self.measurement_layout.add_measurement_widget(name, x, y, Y, values)

        parent = self.measurement_layout.parentWidget()
        while parent:
            if hasattr(parent, 'gamut_chart_widget') and hasattr(parent, 'ranking_widget'):
                parent.gamut_chart_widget.update_charts()
                parent.ranking_widget.update_ranking()
                return
            parent = parent.parentWidget()

    def convert_to_xyY(self, spectrum):
        wavelengths = list(range(400, 400 + 10 * len(spectrum), 10))
        shape = SpectralShape(400, 700, 10)
        sd = SpectralDistribution(dict(zip(wavelengths, spectrum)), shape)

        illuminant = SDS_ILLUMINANTS['C'].copy().align(shape)
        cmfs = MSDS_CMFS['CIE 1931 2 Degree Standard Observer'].copy().align(shape)

        try:
            xyz = sd_to_XYZ(sd, cmfs, illuminant)
            xyy = XYZ_to_xyY(xyz)
            return xyy[0], xyy[1], xyy[2]
        except Exception as e:
            print(f"Error converting to xyY: {e}")
            return 0, 0, 0

    def stop_listening(self):
        self.measurement_layout.timer.stop()
        self.measurement_layout.label.setText("Listening stopped.")
        self.worker.stop()

class SerialWorker(QThread):
    data_received = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        try:
            self.ser = serial.Serial('COM8', 9600, timeout=1)
            while self.running:
                raw_data = self.ser.read(260)
                if len(raw_data) < 260:
                    continue
                values = self.process_raw_data(raw_data)
                self.data_received.emit(values)
                if values:
                    break
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
        except Exception as e:
            print(f"Error reading data: {e}")
        finally:
            if self.ser:
                self.ser.close()

    def process_raw_data(self, raw_data):
        data = raw_data[10:]
        values = [struct.unpack('>f', data[i:i + 4])[0] for i in range(0, len(data) - len(data) % 4, 4)]
        return values[:31]

    def stop(self):
        self.running = False
        self.wait()
