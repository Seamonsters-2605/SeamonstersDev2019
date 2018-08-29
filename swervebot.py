import math
import wpilib
import ctre
import seamonsters as sea

# rotate motor: 3138 ticks per rotation

class SwerveBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        wheelADriveTalon = ctre.WPI_TalonSRX(1)
        wheelARotateTalon = ctre.WPI_TalonSRX(0)

        wheelBDriveTalon = ctre.WPI_TalonSRX(3)
        wheelBRotateTalon = ctre.WPI_TalonSRX(2)

        for talon in [wheelADriveTalon, wheelARotateTalon,
                      wheelBDriveTalon,wheelBRotateTalon]:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        wheelADrive = sea.AngledWheel(wheelADriveTalon,.75, .75, 0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=12)
        wheelBDrive = sea.AngledWheel(wheelBDriveTalon,-.75,.75,0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=12)

        wheelARotate = sea.SwerveWheel(wheelADrive, wheelARotateTalon,
                                       1612.8, True)
        wheelBRotate = sea.SwerveWheel(wheelBDrive,wheelBRotateTalon,
                                       1612.8, True)

        self.superDrive = sea.SuperHolonomicDrive()

        for wheelrotate in [wheelARotate,wheelBRotate]:
            self.superDrive.addWheel(wheelrotate)

        for wheel in self.superDrive.wheels:
            wheel.driveMode = ctre.ControlMode.PercentOutput

    def teleop(self):
        while True:
            mag = sea.deadZone(self.joystick.getMagnitude())
            mag *= 4 # maximum feet per second
            direction = -self.joystick.getDirectionRadians() - math.pi/2
            turn = sea.deadZone(self.joystick.getTwist())
            turn *= math.radians(120) # maximum radians per second

            self.superDrive.drive(mag, direction, turn)

            if self.joystick.getRawButton(4):
                for wheel in self.superDrive.wheels:
                    wheel.driveMode = ctre.ControlMode.PercentOutput
            if self.joystick.getRawButton(3):
                for wheel in self.superDrive.wheels:
                    wheel.driveMode = ctre.ControlMode.Velocity
            if self.joystick.getRawButton(5):
                for wheel in self.superDrive.wheels:
                    wheel.driveMode = ctre.ControlMode.Position

            yield

if __name__ == "__main__":
    wpilib.run(SwerveBot)
