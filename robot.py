import math
import wpilib
import ctre
import navx
import seamonsters as sea
import drivetrain
import dashboard

class CompetitionBot2019(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        self.superDrive = drivetrain.initDrivetrain()
        self.setDriveMode(ctre.ControlMode.PercentOutput)
        self.robotOrigin = None # for encoder-based position tracking

        self.ahrs = navx.AHRS.create_spi()

        self.app = None # dashboard
        sea.startDashboard(self, dashboard.CompetitionBotDashboard)
    
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

    def teleop(self):
        self.resetPositions()
        if self.app is not None:
            self.app.clearEvents()

        while True:
            if self.app is not None:
                self.app.doEvents()

            mag = sea.deadZone(self.joystick.getMagnitude())
            mag *= 3 # maximum feet per second
            direction = -self.joystick.getDirectionRadians() + math.pi/2
            turn = -sea.deadZone(self.joystick.getRawAxis(3))
            turn *= math.radians(120) # maximum radians per second

            self.superDrive.drive(mag, direction, turn)

            yield

if __name__ == "__main__":
    wpilib.run(CompetitionBot2019)
