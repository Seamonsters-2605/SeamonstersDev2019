import math
import remi.gui as gui
import seamonsters as sea

class SwerveBotDashboard(sea.Dashboard):

    def main(self, robot, appCallback):
        self.robot = robot

        root = gui.VBox(width=600)

        fieldWidth = 500
        fieldHeight = 450
        self.fieldSvg = gui.Svg(fieldWidth, fieldHeight)
        root.append(self.fieldSvg)
        self.arrow = gui.SvgPolyline()
        self.fieldSvg.append(self.arrow)
        self.arrow.add_coord(0, 0)
        self.arrow.add_coord(30, 30)
        self.arrow.add_coord(-30, 30)
        self.arrow.style['fill'] = 'gray'

        self.robotX = fieldWidth / 2
        self.robotY = fieldHeight / 2
        self.robotAngle = 0
        self.updateRobotPosition()

        appCallback(self)
        return root

    def moveRobot(self, magnitude, direction, turn):
        self.robotX += magnitude * math.cos(direction + self.robotAngle)
        self.robotY -= magnitude * math.sin(direction + self.robotAngle)
        self.robotAngle += math.degrees(turn) / 50.0
        self.updateRobotPosition()

    def updateRobotPosition(self):
        self.arrow.attributes['transform'] = "translate(%s,%s) rotate(%s)" \
            % (self.robotX, self.robotY, self.robotAngle)
