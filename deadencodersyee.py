import wpilib
import ctre
import seamonsters as sea

class MyRobot (wpilib.IterativeRobot):

    def robotInit(self):
        self.talon = ctre.WPI_TalonSRX(0)
        self.talon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder,0,0)

        self.oldnumber = 0
        self.tick = 0

    def teleopPeriodic(self):
        newnumber = self.talon.getSelectedSensorPosition(0)
        if abs(newnumber) + 1 == self.oldnumber or abs(newnumber) - 1 == self.oldnumber or abs(newnumber) == self.oldnumber:
            self.tick += 1
            self.oldnumber = newnumber
        if not abs(newnumber) + 1 == self.oldnumber or not abs(newnumber) - 1 == self.oldnumber or not abs(newnumber) == self.oldnumber:
            self.tick == 0
        if self.tick == 50:
            print ("It dead broder")

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)