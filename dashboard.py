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
        zeroSteeringBtn.set_on_click_listener(self.queuedEvent(robot.c_zeroSteering))
        root.append(zeroSteeringBtn)

        appCallback(self)
        return root
