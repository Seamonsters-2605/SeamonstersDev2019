import wpilib

class Pneumatics(wpilib.IterativeRobot):

    def robotInit(self):
        self.pneu = wpilib.Solenoid(0)
        self.Joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        if self.Joystick.getRawButton(8):
            self.pneu.set(True)
        if self.Joystick.getRawButton(7):
            self.pneu.set(False) 

if __name__ == "__main__":
    wpilib.run(Pneumatics, physics_enabled = True)