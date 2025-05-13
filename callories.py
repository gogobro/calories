from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import ObjectProperty


class CalorieCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super(CalorieCalculator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)

        # Пол
        self.add_widget(Label(text='Пол:', size_hint=(1, None), height=dp(30)))
        self.gender = Spinner(
            text='Мужской',
            values=('Мужской', 'Женский'),
            size_hint=(1, None),
            height=dp(40))
        self.add_widget(self.gender)

        # Возраст
        self.add_widget(Label(text='Возраст (лет):', size_hint=(1, None), height=dp(30)))
        self.age_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=dp(40))
        self.add_widget(self.age_input)

        # Рост
        self.add_widget(Label(text='Рост (см):', size_hint=(1, None), height=dp(30)))
        self.height_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=dp(40))
        self.add_widget(self.height_input)

        # Вес
        self.add_widget(Label(text='Вес (кг):', size_hint=(1, None), height=dp(30)))
        self.weight_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=dp(40))
        self.add_widget(self.weight_input)

        # Физическая активность
        self.add_widget(Label(text='Физическая активность:', size_hint=(1, None), height=dp(30)))
        self.activity = Spinner(
            text='Средняя активность',
            values=(
                'Минимальная (сидячий образ жизни)',
                'Низкая (легкие упражнения 1-3 раза в неделю)',
                'Средняя (тренировки 3-5 раз в неделю)',
                'Высокая (интенсивные тренировки 6-7 раз в неделю)',
                'Очень высокая (тяжелая физическая работа или спорт)'),
            size_hint=(1, None),
            height=dp(40))
        self.add_widget(self.activity)

        # Кнопка расчета
        self.calculate_btn = Button(
            text='Рассчитать норму калорий',
            size_hint=(1, None),
            height=dp(50))
        self.calculate_btn.bind(on_press=self.calculate)
        self.add_widget(self.calculate_btn)

        # Результат
        self.result = Label(
            text='',
            size_hint=(1, None),
            height=dp(100),  # Увеличили высоту для трёх строк
            font_size=dp(16),
            bold=True,
            halign='left',
            valign='top')
        self.add_widget(self.result)

    def calculate(self, instance):
        try:
            # Получаем данные
            age = int(self.age_input.text)
            height = int(self.height_input.text)
            weight = int(self.weight_input.text)
            gender = self.gender.text
            activity = self.activity.text

            # Рассчитываем базовый метаболизм (BMR)
            if gender == 'Мужской':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            # Учитываем уровень активности
            activity_factors = {
                'Минимальная (сидячий образ жизни)': 1.2,
                'Низкая (легкие упражнения 1-3 раза в неделю)': 1.375,
                'Средняя (тренировки 3-5 раз в неделю)': 1.55,
                'Высокая (интенсивные тренировки 6-7 раз в неделю)': 1.725,
                'Очень высокая (тяжелая физическая работа или спорт)': 1.9
            }

            maintenance = int(bmr * activity_factors[activity])
            loss = int(maintenance * 0.85)  # -15% для похудения
            gain = int(maintenance * 1.15)  # +15% для набора

            self.result.text = (
                f"Для похудения: {loss} ккал/день\n"
                f"Для поддержания: {maintenance} ккал/день\n"
                f"Для набора массы: {gain} ккал/день"
            )

        except ValueError:
            self.result.text = 'Пожалуйста, заполните все поля корректно!'
        except KeyError:
            self.result.text = 'Пожалуйста, выберите уровень активности'


class CalorieApp(App):
    def build(self):
        return CalorieCalculator()


if __name__ == '__main__':
    CalorieApp().run()