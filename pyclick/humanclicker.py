import pyautogui
from pyclick.humancurve import HumanCurve
from random import triangular

def setup_pyautogui():
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0.015  # Default: 0.1

setup_pyautogui()

class HumanClicker():
    def __init__(self):
        pass
    def move(self, toPoint, duration=0, humanCurve=None):
        duration = triangular(0.1,0.9)
        # print(f"Mouse duration={duration:.2f}")
        fromPoint = pyautogui.position()
        if not humanCurve:
            humanCurve = HumanCurve(fromPoint, toPoint)

        # from pprint import pprint
        # pprint(humanCurve.points)

        pyautogui.PAUSE = duration / len(humanCurve.points)
        for point in humanCurve.points:
            # print point
            # pyautogui.moveTo(point)
            pyautogui.dragTo(point,button='left')


    def click(self,x=None,y=None,button='left', clicks=1, duration=0,interval=0.25):
        for _ in range(clicks):
            interval = triangular(0.05,0.4)
            # print(f"Click interval={interval:.2f}")
            if x == None:
                pyautogui.click(button=button, clicks=clicks, interval=interval)
            else:
                if pyautogui.position() != (x,y):
                    self.move((x,y))
                pyautogui.click(button=button, clicks=1, duration=duration,interval=interval)



if __name__ == '__main__':

    # initialize HumanClicker object
    hc = HumanClicker()

    # move the mouse to position (100,100) on the screen in approximately 2 seconds
    hc.move((100, 100), 2)

    # mouse click(left button)
    # hc.click()