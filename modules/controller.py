import pygame

def controller_present():
    return pygame.joystick.get_count()

class Controller(object):
    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

    def listen(self):
        """
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
        """

        return [self.button_data, self.axis_data, self.hat_data]

controller = None
def controller_main():
    global controller
    controller = Controller()
    controller.init()
