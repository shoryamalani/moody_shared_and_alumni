from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Line
from tkinter import colorchooser
import random
from kivy.uix.button import Button

# RGBA = Red, Green, Blue, Opacity
color_value = [1, 1, 1]


def color_change(r, g, b):
    color_value.clear()
    color_value.append(r)
    color_value.append(g)
    color_value.append(b)


class ParentWindow(Widget):
    color = color_value

    def btn(self):
        color_change(1, 0, 0)

    def btn2(self):
        color_change(0, 1, 0)

    def btn3(self):
        color_change(0, 0, 1)

    def btn4(self):
        color_change(1, 1, 1)


class PaintWindow(Widget):
    def on_touch_down(self, touch):
        self.canvas.add(Color(rgb=color_value))
        touch.ud['line'] = Line(points=(touch.x, touch.y))
        self.canvas.add(touch.ud['line'])

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class PaintApp(App):
    def build(self):
        return ParentWindow()


PaintApp().run()
