import wpilib
import ctre
import seamonsters as sea

class MyRobot (wpilib.IterativeRobot):

    def robotInit(self):
        self.talon = ctre.WPI_TalonSRX(0)
        self.talon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder)
        self.values = []

    def teleopPeriodic(self):
        if len(self.values) == 50:
            last_value = self.values.pop()
        new_value = self.talon.getSelectedSenosrPosition(0)
        if abs(ne_value - last_value) <= 1:
            print ("Dead encoder")

if name == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)