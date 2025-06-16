from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
import sqlite3
from kivy.uix.screenmanager import ScreenManager


class BD_food(MDScreen):
    def __init__(self, name, window_count, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = 'table.db'
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        self.label = MDLabel(pos_hint={"center_x": 0.5, "center_y": 0.6}, size_hint=(0.8, 0.1))
        self.back = MDRectangleFlatButton(text="Назад", pos_hint={"center_x": 0.85, "center_y": 0.1},
                                   size_hint=(0.1, 0.05), line_color="red", text_color="white")
        self.dadd = MDRaisedButton(text="Добавить", pos_hint={"center_x": 0.7, "center_y": 0.4},
                                   size_hint=(0.15, 0.075))
        self.dremove = MDRectangleFlatButton(text="Удалить",
                                             pos_hint={"center_x": 0.3, "center_y": 0.4}, size_hint=(0.15, 0.075))
        self.dish = MDTextField(hint_text='Введите', pos_hint={"center_x": 0.33, "center_y": 0.8}, mode="round", size_hint_x=0.6)
        self.ccal = MDTextField(hint_text='ККалории', pos_hint={"center_x": 0.82, "center_y": 0.8}, mode="round",
                                size_hint_x=0.3)
        self.dadd.bind(on_press=self.bd_add)
        self.dremove.bind(on_press=self.bd_remove)
        self.back.bind(on_press=self.prev_window)
        self.add_widget(self.label)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.add_widget(self.dadd)
        self.add_widget(self.dremove)
        self.add_widget(self.ccal)
        self.add_widget(self.back)
        self.add_widget(self.dish)

    def bd_add(self, k):
        if not self.dish.text or not self.ccal.text:
            self.label.text = 'Пожалуйста введите блюдо, которое хотите добавить, и его каллорийность.'
        else:
            try:
                int(self.ccal.text)
                self.cur.execute(f"""INSERT or REPLACE INTO food(name, ccal) VALUES('{self.dish.text}', {int(self.ccal.text)})""")
                self.con.commit()
                self.label.text = 'Блюдо успешно добавлено!'
            except ValueError:
                self.label.text = 'Введите корректное значение каллорий'

    def bd_remove(self, k):
        if not self.dish.text:
            self.label.text = 'Пожалуйста введите блюдо, которое хотите удалить.'
        else:
            self.cur.execute(f"""DELETE from food WHERE name = '{self.dish.text}'""")
            self.con.commit()
            self.label.text = 'Блюдо успешно удалено!'

    def prev_window(self, instance):
        current = int(self.name)
        prev_window = str(current - 1) if current > 1 else str(self.window_count)
        self.manager.current = prev_window

class CalorieApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BD_food(name='1', window_count=1))

        return sm


if __name__ == '__main__':
    CalorieApp().run()

