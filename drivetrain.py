import ctre
import seamonsters as sea

def initDrivetrain():
    superDrive = sea.SuperHolonomicDrive()
    _makeSwerveWheel(superDrive, 1, 0,  .75,  .75, 1612.8, True)
    _makeSwerveWheel(superDrive, 3, 2, -.75,  .75, 1612.8, True)
    _makeSwerveWheel(superDrive, 5, 4,    0, -.75, 1680,   True)
    sea.setSimulatedDrivetrain(superDrive)
    return superDrive

def _makeSwerveWheel(superDrive, driveTalonNum, rotateTalonNum, xPos, yPos,
                    encoderCountsPerRev, reverseSteerMotor):
    driveTalon = ctre.WPI_TalonSRX(driveTalonNum)
    rotateTalon = ctre.WPI_TalonSRX(rotateTalonNum)
    driveTalon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
    rotateTalon.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)

    angledWheel = sea.AngledWheel(driveTalon, xPos, yPos, 0,
                                    encoderCountsPerFoot=31291.1352,
                                    maxVoltageVelocity=16)

    swerveWheel = sea.SwerveWheel(angledWheel, rotateTalon, encoderCountsPerRev, reverseSteerMotor)

    superDrive.addWheel(swerveWheel)
