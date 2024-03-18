import kivy
from kivy.app import App
from kivy.core.window import Window  # Window Setting
from kivy.core.text import LabelBase, DEFAULT_FONT  # Font Setting
from kivy.resources import resource_add_path  # Font Setting
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

# import mylog
import time
from os.path import dirname, join
import threading
import serial

# kivy version
kivy.require('2.0.0')

# Window Size
# Window.fullscreen = 'auto'  # 全屏并使用当前屏幕分辨率
Window.size = (1024, 600)

# Font Setting
resource_add_path('data/Fonts')
LabelBase.register(DEFAULT_FONT, '苹方.ttf')

# 当前目录
current_dir = dirname(__file__)
print(current_dir)

# 当前时间
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(current_time)

# 连接串口
try:
    print('尝试连接串口...')
    ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=5)
except:
    print('未成功连接串口！')
else:
    print('串口连接成功！')


# 最底层背景
class ShowScreen(FloatLayout):
    pass


class MyClock(AnchorLayout):
    pass


# 小组件展示
class ShowWidgets(BoxLayout):
    table_height = 45

    def __init__(self):
        super(ShowWidgets, self).__init__()

    # 滑块被按下
    def slider_down(self, slider):
        print("滑块被按下了，当前值为:", slider.value)

    # def slider_move(self, slider):
    #     """移动事件"""
    #     print("滑块被移动了:", slider.value)

    def lift_up(self, up_button):
        print('置物台上升')
        self.ids.lift_up_img.source = 'data/Icons/touch-up.png'

        height = int(ser.readline())
        if height < 100:
            self.table_height += 1
            ser.write(b's')
        else:
            print('已是最大高度！')
        height = int(ser.readline())
        self.ids.th_data.text = '{:d} cm'.format(height)

    def lift_up_release(self):
        self.ids.lift_up_img.source = 'data/Icons/up.png'
        print('UP按钮释放')

    def lift_down(self, down_button):
        print('置物台下降')
        self.ids.lift_down_img.source = 'data/Icons/touch-down.png'

        if self.table_height >= 46:
            self.table_height -= 1
            ser.write('s')
        else:
            print('已是最低高度！')

        self.ids.th_data.text = '{:d} cm'.format(self.table_height)

    def lift_down_release(self):
        self.ids.lift_down_img.source = 'data/Icons/down.png'
        print('DOWN按钮释放')

    def hold_press(self, dt):
        pass


# 主程序
class ControllerApp(App):

    def __init__(self, **kwargs):
        super(ControllerApp, self).__init__(**kwargs)

    def build(self):
        # 窗口图标设置
        self.icon = 'data/Icons/dash_board.png'

        Clock.schedule_interval(self._update_clock, 1 / 60.)

        root = ShowScreen()
        root.add_widget(ShowWidgets())
        root.add_widget(MyClock())

        return root

    def send(self, data: str = None):
        return ser.write(data)

    def receive(self, data: str = None):
        return ser.readline(data)

    def _update_clock(self, dt):
        self.time = time.time()


def start():
    return ControllerApp().run()


if __name__ == '__main__':
    t2 = threading.Thread(target=start)
    t2.run()
