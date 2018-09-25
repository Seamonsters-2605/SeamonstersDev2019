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
        self.talon.set(1)
        if newnumber + 1 == self.oldnumber or newnumber - 1 == self.oldnumber or newnumber == self.oldnumber:
            self.tick += 1
        else:
            self.tick = 0
            self.oldnumber = newnumber
        if self.tick >= 50:
            print ("It dead broder")
            self.talon.set(0)
        print (newnumber)
        print (self.oldnumber)
        print (self.tick)
if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)