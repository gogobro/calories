from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import random
import sqlite3


class ThirdScreen(MDScreen):
    def __init__(self, name, window_count, **kwargs):
        super().__init__(name=name, **kwargs)
        self.window_count = window_count
        self.data = None

        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Кнопка "Рассчитать"
        self.calc_button = MDFillRoundFlatButton(
            text="Рассчитать",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.1, 0.6, 0.2, 1),
            on_release=self.calc
        )
        layout.add_widget(self.calc_button)

        # Результат
        self.output_label = MDLabel(
            text="Здесь будет результат...",
            halign='center',
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(100)
        )
        layout.add_widget(self.output_label)

        # Кнопки перехода
        nav_buttons = MDBoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))

        self.btn_prev = MDFillRoundFlatButton(
            text='Назад',
            size_hint=(0.5, 1),
            md_bg_color=(0.92, 0.26, 0.21, 1)
        )
        self.btn_prev.bind(on_release=self.prev_window)

        self.btn_next = MDFillRoundFlatButton(
            text='Вперед',
            size_hint=(0.5, 1),
            md_bg_color=(0.2, 0.65, 0.32, 1)
        )
        self.btn_next.bind(on_release=self.next_window)

        nav_buttons.add_widget(self.btn_prev)
        nav_buttons.add_widget(self.btn_next)
        layout.add_widget(nav_buttons)

        self.add_widget(layout)

    # Подборка питания учитывая норму
    def calc(self, k):
        try:
            tolerance = 0.1
            max_attempts = 1000
            target = int(self.data)
            db = 'table.db'
            con = sqlite3.connect(db)
            cur = con.cursor()
            s = cur.execute("""SELECT * FROM FOOD""")
            con.commit()
            numbers = [i for i in s]
            for _ in range(max_attempts):
                combo = []
                remaining = target
                shuffled = numbers.copy()
                random.shuffle(shuffled)

                for num in shuffled:
                    if num[2] <= remaining * (1 + tolerance):
                        combo.append(num)
                        remaining -= num[2]
                        if abs(remaining) <= target * tolerance:
                            return self.change(combo, 1)
                        if remaining < 0:
                            break
            return self.change(None, 2)
        except Exception as e:
            return self.change(e, 3)

    # Вывод новго питания или вывод его отсутствия
    def change(self, rez, state):
        if state == 1:
            sps = []
            for i in rez:
                sps.append(f'{i[1]} - {i[2]}')
            self.output_label.text = ', '.join(sps)
        elif state == 2:
            self.output_label.text = 'Пожалуйста добавьте больше еды, чтобы составить вашу программу питания на сегодня'
        else:
            self.output_label.text = f'Рассчитайте калорийность корректно {rez}'

    # Паттерн Observer - наблюдатель
    def on_data_changed(self, new_data):
        self.data = new_data
        self.output_label.text = f'Рассчитать рацион для поддержания веса в размере {new_data}?'

    def prev_window(self, instance):
        current = int(self.name)
        prev_window = str(current - 1) if current > 1 else str(self.window_count)
        self.manager.current = prev_window

    def next_window(self, instance):
        current = int(self.name)
        next_window = str(current + 1) if current < self.window_count else '1'
        self.manager.current = next_window

# Запуск данного окна в режиме приложения (только для просмотра)
class CalorieApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ThirdScreen(name='1', window_count=1))

        return sm


if __name__ == '__main__':
    CalorieApp().run()