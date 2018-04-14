import remi
import remi.gui as gui
import queue

def HBoxWith(contents, **kwargs):
    box = gui.HBox(**kwargs)
    for widget in contents:
        box.append(widget)
    return box

def VBoxWith(contents, **kwargs):
    box = gui.VBox(**kwargs)
    for widget in contents:
        box.append(widget)
    return box

class MotorTester(remi.App):
    def __init__(self, *args):
        self.eventQueue = queue.Queue()

        super(MotorTester, self).__init__(*args)

    def main(self, robot, appCallback):
        self.robot = robot

        root = gui.VBox(width=600)

        title = gui.Label('Motor Tester')
        title.style['margin'] = '24px'
        title.style['font-size'] = '36px'
        title.style['font-weight'] = 'bold'
        root.append(title)

        talonBox = gui.SpinBox(default_value='0', min=0, max=3, step=1)
        talonBox.set_on_change_listener(self.queuedEvent(robot.c_setTalon))
        root.append(HBoxWith((
            gui.Label('Talon:&nbsp;'),
            talonBox
        )))

        self.outputVoltageLbl = gui.Label('')
        root.append(HBoxWith((
            gui.Label('Output voltage:&nbsp;'),
            self.outputVoltageLbl
        )))

        self.outputCurrentLbl = gui.Label('')
        root.append(HBoxWith((
            gui.Label('Output current:&nbsp;'),
            self.outputCurrentLbl
        )))

        self.encoderPositionLbl = gui.Label('')
        root.append(HBoxWith((
            gui.Label('Encoder position:&nbsp;'),
            self.encoderPositionLbl
        )))

        self.encoderVelocityLbl = gui.Label('')
        root.append(HBoxWith((
            gui.Label('Encoder velocity:&nbsp;'),
            self.encoderVelocityLbl
        )))

        controlTabBox = gui.TabBox(width='100%')
        root.append(controlTabBox)

        controlTabBox.add_tab(gui.Widget(), 'Disabled',
            self.queuedEvent(robot.c_updateDisabled))

        self.outputSlider = gui.Slider(default_value="0", min=-100, max=100,
                                       width='100%')
        controlTabBox.add_tab(self.outputSlider, 'Percent Output',
                              self.c_percentOutputTab)
        self.outputSlider.set_on_change_listener(
            self.queuedEvent(robot.c_updatePercentOutput))

        velocityFrame = gui.HBox(width='100%')
        controlTabBox.add_tab(velocityFrame, 'Velocity', self.c_velocityTab)
        self.velocityOutputSlider = gui.Slider(default_value="0",
                                               min=-100, max=100, width='100%')
        velocityFrame.append(self.velocityOutputSlider)
        self.maxVelocityBox = gui.SpinBox(
            default_value='8000', min=0, max=1000000, step=100, width='100')
        velocityFrame.append(self.maxVelocityBox)
        self.velocityOutputSlider.set_on_change_listener(
            self.queuedEvent(robot.c_updateVelocity),
            self.velocityOutputSlider, self.maxVelocityBox)
        self.maxVelocityBox.set_on_change_listener(
            self.queuedEvent(robot.c_updateVelocity),
            self.velocityOutputSlider, self.maxVelocityBox)

        self.offsetBox = gui.SpinBox('0', -1000000, 1000000, 100)
        holdButton = gui.Button('Hold', width='100')
        holdButton.set_on_click_listener(
            self.queuedEvent(robot.c_updatePosition), self.offsetBox)
        controlTabBox.add_tab(HBoxWith((
            gui.Label('Offset:&nbsp;'),
            self.offsetBox,
            holdButton
        )), 'Hold Position', self.queuedEvent(robot.c_updateDisabled))

        # margin
        root.append(gui.HBox(height=10))

        appCallback(self)
        return root

    def c_percentOutputTab(self):
        self.outputSlider.set_value('0')
        self.queuedEvent(self.robot.c_updatePercentOutput)(self.outputSlider)

    def c_velocityTab(self):
        self.velocityOutputSlider.set_value('0')
        self.queuedEvent(self.robot.c_updateVelocity) \
            (None, None, self.velocityOutputSlider, self.maxVelocityBox)

    def queuedEvent(self, event):
        def queueTheEvent(*args, **kwargs):
            def doTheEvent():
                print("Event:", event.__name__)
                event(*args, **kwargs)
            self.eventQueue.put(doTheEvent)
        return queueTheEvent

def main(robot, appCallback):
    remi.start(MotorTester, userdata=(robot, appCallback,))
