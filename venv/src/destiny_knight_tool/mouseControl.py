from pymouse import PyMouseEvent


class DetectMouseClick(PyMouseEvent):

    _mousePos = [];

    def __init__(self):
        PyMouseEvent.__init__(self)
        self._mousePos = []

    def click(self, x, y, button, press):
        if button == 1:
            if press:
               self._mousePos = [x,y];
               self.stop()
               #print(self._mousePos)

def getPosition():
    O = DetectMouseClick()
    O.run()
    return O._mousePos

