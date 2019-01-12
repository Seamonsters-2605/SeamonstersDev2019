import ctre
import seamonsters as sea

ROBOT_WIDTH = 21.9950 / 12 # feet
ROBOT_LENGTH = 21.9950 / 12

def initDrivetrain():
    superDrive = sea.SuperHolonomicDrive()
    _makeSwerveWheel(superDrive, 1, 0,  ROBOT_WIDTH/2,  ROBOT_LENGTH/2, True)
    _makeSwerveWheel(superDrive, 3, 2, -ROBOT_WIDTH/2,  ROBOT_LENGTH/2, True)
    _makeSwerveWheel(superDrive, 5, 4,  ROBOT_WIDTH/2, -ROBOT_LENGTH/2, True)
    _makeSwerveWheel(superDrive, 7, 6, -ROBOT_WIDTH/2, -ROBOT_LENGTH/2, True)
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

    swerveWheel = sea.SwerveWheel(angledWheel, rotateTalon, 1612.8, reverseSteerMotor)

    superDrive.addWheel(swerveWheel)
