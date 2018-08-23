import wpilib
import ctre
import seamonsters as sea
import threading
import motortest_app

class MotorTestBot(sea.GeneratorBot):

    def robotInit(self):
        self.talons = [ctre.WPI_TalonSRX(i)
            for i in range(0, motortest_app.MotorTester.MAX_TALON + 1)]
        for talon in self.talons:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        self.joy = wpilib.Joystick(0)

        appReadyEvent = threading.Event()
        def appCallback(app):
            self.app = app
            appReadyEvent.set()
        thread = threading.Thread(target=motortest_app.main,
                                  args=(self, appCallback))
        thread.daemon = True
        thread.start()
        print("Waiting for app to start...")
        appReadyEvent.wait()
        print("App started!")

    def teleop(self):
        # clear event queue
        while not self.app.eventQueue.empty():
            self.app.eventQueue.get()

        self.talon = self.talons[0]

        while True:
            yield
            while not self.app.eventQueue.empty():
                event = self.app.eventQueue.get()
                event()
            self.updateTalonLog()

    def c_setTalon(self, widget, value):
        self.talon.disable()
        try:
            self.talon = self.talons[int(value)]
        except IndexError: pass

    def c_updateDisabled(self):
        self.talon.disable()

    def c_updatePercentOutput(self, widget, value=None):
        value = float(widget.get_value()) / 100.0
        self.talon.set(ctre.ControlMode.PercentOutput, value)

    def c_updateVelocity(self, widget, value, slider, scaleBox):
        value = float(slider.get_value()) * float(scaleBox.get_value()) / 100.0
        self.talon.set(ctre.ControlMode.Velocity, value)

    def c_updatePosition(self, button, spinBox):
        value = self.talon.getSelectedSensorPosition(0) + \
                int(spinBox.get_value())
        self.talon.set(ctre.ControlMode.Position, value)

    def updateTalonLog(self):
        talon = self.talon
        try:
            self.app.outputVoltageLbl.set_text(
                str(talon.getMotorOutputVoltage()))
            self.app.outputCurrentLbl.set_text(
                str(talon.getOutputCurrent()))
            self.app.encoderPositionLbl.set_text(
                str(talon.getSelectedSensorPosition(0)))
            self.app.encoderVelocityLbl.set_text(
                str(talon.getSelectedSensorVelocity(0)))
        except AssertionError:
            pass

if __name__ == "__main__":
    wpilib.run(MotorTestBot)
