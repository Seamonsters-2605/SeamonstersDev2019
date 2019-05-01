import math
import wpilib
import ctre
import seamonsters as sea
import swervebot_app
import navx

#A swerve drive meant to be controlled with a gamepad/xbox controller where it will face the direction of 1 joystick
#and drive towards the direction of the other stick.

# rotate motor: 3138 ticks per rotation

class SwerveBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        self.superDrive = sea.SuperHolonomicDrive()
        sea.setSimulatedDrivetrain(self.superDrive)

        self.makeSwerveWheel(1, 0, .75, .75, 1612.8, True)
        self.makeSwerveWheel(3, 2, -.75, .75, 1612.8, True)
        self.makeSwerveWheel(5, 4, 0, -.75, 1680, True) # 1670, 1686, 1680
        self.setDriveMode(ctre.ControlMode.PercentOutput)

        self.robotOrigin = None

        self.app = None
        sea.startDashboard(self, swervebot_app.SwerveBotDashboard)
        self.ahrs = navx.AHRS.create_spi()

        self.pathFollower = sea.PathFollower(self.superDrive, self.ahrs)

    def makeSwerveWheel(self, driveTalonNum, rotateTalonNum, xPos, yPos,
                        encoderCountsPerRev, reverseSteerMotor):
        driveTalon = ctre.WPI_TalonSRX(driveTalonNum)
        rotateTalon = ctre.WPI_TalonSRX(rotateTalonNum)
        driveTalon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        rotateTalon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)

        angledWheel = sea.AngledWheel(driveTalon, xPos, yPos, 0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=16)

        swerveWheel = sea.SwerveWheel(angledWheel, rotateTalon, encoderCountsPerRev, reverseSteerMotor)

        self.superDrive.addWheel(swerveWheel)
    
    def setDriveMode(self, mode):
        print("Drive mode:", mode)
        for wheel in self.superDrive.wheels:
            if isinstance(wheel, sea.SwerveWheel):
                wheel.angledWheel.driveMode = mode

    def resetPositions(self):
        for wheel in self.superDrive.wheels:
            wheel.resetPosition()

    def autonomous(self):
        self.resetPositions()
        self.setDriveMode(ctre.ControlMode.Position)
        data = sea.readDataFile("testpath.txt")
        yield from self.pathFollower.followPathData(data)

    def teleop(self):     
        self.resetPositions()
        if self.app is not None:
            self.app.clearEvents()
        # reset joystick buttons
        self.joystick.getRawButtonPressed(3)
        self.joystick.getRawButtonPressed(4)
        self.joystick.getRawButtonPressed(5)
        while True:
            if self.app is not None:
                self.app.doEvents()
            
            self.pathFollower.updateRobotPosition()            
            angularOffset = sea.circleDistance(self.pathFollower.robotAngle,  math.atan2(sea.deadZone(-self.joystick.getRawAxis(4), 0.3), sea.deadZone(-self.joystick.getRawAxis(3), 0.3)))
            mag = sea.deadZone(self.joystick.getMagnitude())
            mag *= 7 # maximum feet per second
            direction = -self.joystick.getDirectionRadians() + math.pi/2
            direction -= self.pathFollower.robotAngle # field oriented mode
            turn = angularOffset * math.radians(270) # maximum radians per second

            self.superDrive.drive(mag, direction, turn)

            if self.app is not None:
                moveMag, moveDir, moveTurn, self.robotOrigin = \
                    self.superDrive.getRobotPositionOffset(self.robotOrigin)
                self.app.moveRobot(moveMag, moveDir, moveTurn)
            if self.joystick.getRawButtonPressed(4):
                self.setDriveMode(ctre.ControlMode.PercentOutput)
            if self.joystick.getRawButtonPressed(3):
                self.setDriveMode(ctre.ControlMode.Velocity)
            if self.joystick.getRawButtonPressed(5):
                self.setDriveMode(ctre.ControlMode.Position)

            yield

if __name__ == "__main__":
    wpilib.run(SwerveBot)
