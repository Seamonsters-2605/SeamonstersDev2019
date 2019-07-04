import wpilib
import ctre
import seamonsters as sea 
import math

#to be used as an example for offseason training lessons
class PracticeBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        #set up drivetrian
        self.initDrivetrain()

    def initDrivetrain(self):
        #talons
        leftTalon = ctre.WPI_TalonSRX(0)
        rightTalon = ctre.WPI_TalonSRX(1)
        
        #configure talons
        for talon in [leftTalon, rightTalon]:
            talon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)

        #create wheels
        leftWheel = sea.AngledWheel(leftTalon, -1, 0, math.pi/2, 31291.1352, 16)
        rightWheel = sea.AngledWheel(rightTalon, 1, 0, math.pi/2, 31291.1352, 16)

        #add wheels to drivetrain
        self.drivetrain = sea.SuperHolonomicDrive()
        self.drivetrain.addWheel(leftWheel)
        self.drivetrain.addWheel(rightWheel)

        for wheel in self.drivetrain.wheels:
            wheel.driveMode = ctre.ControlMode.PercentOutput

        #sets up drivetrain to work in the simulator
        sea.setSimulatedDrivetrain(self.drivetrain)

        
    def teleop(self):
        while True:
            mag = sea.deadZone(self.joystick.getY())
            mag *= 5 # maximum feet per second
            turn = sea.deadZone(self.joystick.getX())
            turn *= math.radians(300) # maximum radians per second

            self.drivetrain.drive(mag, math.pi/2, turn)
            
            yield

if __name__ == "__main__":
    wpilib.run(PracticeBot)