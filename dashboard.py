import remi.gui as gui
import seamonsters as sea

class CompetitionBotDashboard(sea.Dashboard):

    def main(self, robot, appCallback):
        self.robot = robot

        root = gui.VBox(width=600)

        self.encoderPositionLbl = gui.Label("[encoder position]")
        root.append(self.encoderPositionLbl)
        self.navxPositionLbl = gui.Label("[navx position]")
        root.append(self.navxPositionLbl)
        self.visionPositionLbl = gui.Label("[vision position]")
        root.append(self.visionPositionLbl)

        zeroSteeringBtn = gui.Button("Reset swerve rotations")
        zeroSteeringBtn.onclick.connect(self.queuedEvent(robot.c_zeroSteering))
        root.append(zeroSteeringBtn)

        driveModeBox = gui.HBox()
        root.append(driveModeBox)

        percentOutputBtn = gui.Button("Voltage")
        percentOutputBtn.onclick.connect(self.queuedEvent(robot.c_percentOutputMode))
        driveModeBox.append(percentOutputBtn)
        velocityBtn = gui.Button("Velocity")
        velocityBtn.onclick.connect(self.queuedEvent(robot.c_velocityMode))
        driveModeBox.append(velocityBtn)
        positionBtn = gui.Button("Position")
        positionBtn.onclick.connect(self.queuedEvent(robot.c_positionMode))
        driveModeBox.append(positionBtn)

        appCallback(self)
        return root
