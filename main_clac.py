from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatButton
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from bd_food import BD_food
from nutrition import ThirdScreen


class CalorieCalculator(MDScreen):
    result_text = StringProperty("")

    def __init__(self, name, window_count, **kwargs):
        super().__init__(name=name, **kwargs)
        self.obsers = []
        self.window_count = window_count
        self.layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # Пол
        self.layout.add_widget(MDLabel(text='Пол:', halign='left', size_hint_y=None, height=dp(30)))

        self.gender_btn = MDRectangleFlatButton(
            text='Мужской',
            size_hint=(1, None),
            height=dp(40),
            on_release=self.open_gender_menu
        )
        self.layout.add_widget(self.gender_btn)

        # Возраст
        self.layout.add_widget(MDLabel(text='Возраст (лет):', halign='left', size_hint_y=None, height=dp(30)))
        self.age_input = MDTextField(
            hint_text="Введите возраст",
            input_filter='int',
            size_hint=(1, None),
            height=dp(40)
        )
        self.layout.add_widget(self.age_input)

        # Рост
        self.layout.add_widget(MDLabel(text='Рост (см):', halign='left', size_hint_y=None, height=dp(30)))
        self.height_input = MDTextField(
            hint_text="Введите рост",
            input_filter='int',
            size_hint=(1, None),
            height=dp(40)
        )
        self.layout.add_widget(self.height_input)

        # Вес
        self.layout.add_widget(MDLabel(text='Вес (кг):', halign='left', size_hint_y=None, height=dp(30)))
        self.weight_input = MDTextField(
            hint_text="Введите вес",
            input_filter='int',
            size_hint=(1, None),
            height=dp(40)
        )
        self.layout.add_widget(self.weight_input)

        # Физическая активность
        self.layout.add_widget(MDLabel(text='Физическая активность:', halign='left', size_hint_y=None, height=dp(30)))

        self.activity_btn = MDRectangleFlatButton(
            text='Средняя активность',
            size_hint=(1, None),
            height=dp(40),
            on_release=self.open_activity_menu
        )
        self.layout.add_widget(self.activity_btn)

        # Кнопка расчета
        self.calculate_btn = MDFillRoundFlatButton(
            text='Рассчитать норму калорий',
            size_hint=(1, None),
            height=dp(50),
            on_release=self.calculate
        )
        self.layout.add_widget(self.calculate_btn)

        # Результат
        self.result_label = MDLabel(
            text=self.result_text,
            size_hint=(1, None),
            height=dp(100),
            font_style="H6",
            halign='center',
            theme_text_color="Primary"
        )
        self.layout.add_widget(self.result_label)
        nav_layout = MDBoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))

        # Кнопка "Назад"
        self.btn_prev = MDFillRoundFlatButton(
            text='Назад',
            size_hint=(0.5, 1),
            md_bg_color=(0.92, 0.26, 0.21, 1)  # Красный
        )
        self.btn_prev.bind(on_release=self.prev_window)
        nav_layout.add_widget(self.btn_prev)

        # Кнопка "Вперед"
        self.btn_next = MDFillRoundFlatButton(
            text='Вперед',
            size_hint=(0.5, 1),
            md_bg_color=(0.2, 0.65, 0.32, 1)  # Зеленый
        )
        self.btn_next.bind(on_release=self.next_window)
        nav_layout.add_widget(self.btn_next)

        self.layout.add_widget(nav_layout)
        self.add_widget(self.layout)

        # Инициализация меню после создания всех виджетов
        self.init_menus()

    # Паттерн Observer - Объект
    def attach(self, observer):
        self.obsers.append(observer)

    def init_menus(self):
        # Меню для выбора пола
        self.gender_menu = MDDropdownMenu(
            caller=self.gender_btn,
            items=[
                {"text": "Мужской", "on_release": lambda x="Мужской": self.set_gender(x)},
                {"text": "Женский", "on_release": lambda x="Женский": self.set_gender(x)},
            ],
            width_mult=4,
        )

        # Меню для выбора активности
        self.activity_menu = MDDropdownMenu(
            caller=self.activity_btn,
            items=[
                {"text": "Минимальная (сидячий образ жизни)",
                 "on_release": lambda x="Минимальная": self.set_activity(x)},
                {"text": "Низкая (легкие упражнения 1-3 раза в неделю)",
                 "on_release": lambda x="Низкая": self.set_activity(x)},
                {"text": "Средняя (тренировки 3-5 раз в неделю)",
                 "on_release": lambda x="Средняя": self.set_activity(x)},
                {"text": "Высокая (интенсивные тренировки 6-7 раз в неделю)",
                 "on_release": lambda x="Высокая": self.set_activity(x)},
                {"text": "Очень высокая (тяжелая физическая работа или спорт)",
                 "on_release": lambda x="Очень высокая": self.set_activity(x)},
            ],
            width_mult=4,
        )

    def set_gender(self, gender):
        self.gender_btn.text = gender
        self.gender_menu.dismiss()

    def set_activity(self, activity):
        self.activity_btn.text = activity
        self.activity_menu.dismiss()

    def open_gender_menu(self, instance):
        self.gender_menu.open()

    def open_activity_menu(self, instance):
        self.activity_menu.open()

    def calculate(self, instance):
        try:
            # Получаем данные
            age = int(self.age_input.text)
            height = int(self.height_input.text)
            weight = int(self.weight_input.text)
            gender = self.gender_btn.text
            activity = self.activity_btn.text

            # Рассчитываем базовый метаболизм (BMR)
            if gender == 'Мужской':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            # Учитываем уровень активности
            activity_factors = {
                'Минимальная': 1.2,
                'Низкая': 1.375,
                'Средняя': 1.55,
                'Высокая': 1.725,
                'Очень высокая': 1.9
            }

            maintenance = int(bmr * activity_factors[activity])
            loss = int(maintenance * 0.85)  # -15% для похудения
            gain = int(maintenance * 1.15)  # +15% для набора

            self.result_text = (
                f"Для похудения: {loss} ккал/день\n"
                f"Для поддержания: {maintenance} ккал/день\n"
                f"Для набора массы: {gain} ккал/день"
            )
            self.obsers[0].on_data_changed(str(maintenance))
            self.result_label.text = self.result_text
        except ValueError:
            self.result_text = 'Пожалуйста, заполните все поля корректно!'
            self.result_label.text = self.result_text
        except KeyError:
            self.result_text = 'Пожалуйста, выберите уровень активности'
            self.result_label.text = self.result_text

    def prev_window(self, instance):
        current = int(self.name)
        prev_window = str(current - 1) if current > 1 else str(self.window_count)
        self.manager.current = prev_window

    def next_window(self, instance):
        current = int(self.name)
        next_window = str(current + 1) if current < self.window_count else '1'
        self.manager.current = next_window


# Основное приложение
class CalorieApp(MDApp):
    def __init__(self):
        super().__init__()
        self.calk = CalorieCalculator(name=str(1), window_count=3)
        self.vivod = ThirdScreen(name=str(2), window_count=3)
        self.bd_food = BD_food(name=str(3), window_count=3)
        self.calk.obsers.append(self.vivod)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(self.calk)
        sm.add_widget(self.vivod)
        sm.add_widget(self.bd_food)

        return sm


if __name__ == '__main__':
    CalorieApp().run()