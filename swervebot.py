import math
import wpilib
import ctre
import seamonsters as sea

# rotate motor: 3138 ticks per rotation

class SwerveBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        wheelADriveTalon = ctre.WPI_TalonSRX(11)
        wheelARotateTalon = ctre.WPI_TalonSRX(12)

        wheelBDriveTalon = ctre.WPI_TalonSRX(13)
        wheelBRotateTalon = ctre.WPI_TalonSRX(14)

        wheelCDriveTalon = ctre.WPI_TalonSRX(15)
        wheelCRotateTalon = ctre.WPI_TalonSRX(16)

        for talon in [wheelADriveTalon, wheelARotateTalon,
                      wheelBDriveTalon,wheelBRotateTalon,
                      wheelCDriveTalon,wheelCRotateTalon]:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        wheelADrive = sea.AngledWheel(wheelADriveTalon,0, 1, 0,
                                      encoderCountsPerFoot=6000,
                                      maxVoltageVelocity=12)
        wheelBDrive = sea.AngledWheel(wheelBDriveTalon,1,0,0,
                                      encoderCountsPerFoot=6000,
                                      maxVoltageVelocity=12)
        wheelCDrive = sea.AngledWheel(wheelCDriveTalon,-1,0,0,
                                      encoderCountsPerFoot=6000,
                                      maxVoltageVelocity=12)

        wheelARotate = sea.SwerveWheel(wheelADrive, wheelARotateTalon,
                                       3138, True)
        wheelBRotate = sea.SwerveWheel(wheelBDrive,wheelBRotateTalon,
                                       3138, True)
        wheelCRotate = sea.SwerveWheel(wheelCDrive,wheelCRotateTalon,
                                       3138, True)
        self.superDrive = sea.SuperHolonomicDrive()

        for wheelrotate in [wheelARotate,wheelBRotate,wheelCRotate]:
            self.superDrive.addWheel(wheelrotate)

        for wheel in self.superDrive.wheels:
            wheel.driveMode = ctre.ControlMode.Velocity

    def teleop(self):
        while True:
            mag = sea.deadZone(self.joystick.getMagnitude())
            mag *= 5 # maximum feet per second
            direction = -self.joystick.getDirectionRadians() - math.pi/2
            turn = sea.deadZone(self.joystick.getTwist()
            turn *= math.radians(90) # maximum radians per second

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
