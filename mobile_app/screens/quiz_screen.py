from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivy.metrics import dp

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_success


class QuizScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_data = None
        self.dialog = None

        self.questions_count = 0
        self.correct_count = 0
        self.incorrect_count = 0

        self.total_questions = 10
        self.answered = False
        self.waiting_for_next = False

        self.current_level = None
        self.questions = []
        self.current_question_index = 0

        self.current_buttons = []

        self.build_ui()

    # ================= UI =================

    def build_ui(self):
        from kivymd.uix.scrollview import MDScrollView

        root = MDBoxLayout(orientation="vertical")
        scroll = MDScrollView()

        self.main = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15,
            size_hint_y=None
        )
        self.main.bind(minimum_height=self.main.setter("height"))

        # HEADER
        header = MDCard(
            orientation="vertical",
            padding=20,
            size_hint=(0.95, None),
            height=dp(140),
            pos_hint={"center_x": 0.5},
            md_bg_color="#2196F3"
        )

        self.level_title = MDLabel(
            text="",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )

        title = MDLabel(
            text="🧠 Викторина",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )

        header.add_widget(title)
        header.add_widget(self.level_title)
        self.main.add_widget(header)

        # PROGRESS
        progress_card = MDCard(
            orientation="vertical",
            padding=15,
            size_hint=(0.95, None),
            height=dp(90),
            pos_hint={"center_x": 0.5}
        )

        self.progress_label = MDLabel(
            text="0/0",
            halign="center",
            size_hint_y=None,
            height=dp(25)
        )

        self.progress_bar = MDProgressBar(
            value=0,
            size_hint_y=None,
            height=dp(20)
        )

        progress_card.add_widget(self.progress_label)
        progress_card.add_widget(self.progress_bar)
        self.main.add_widget(progress_card)

        # QUESTION CARD
        self.word_card = MDCard(
            orientation="vertical",
            padding=20,
            spacing=10,
            size_hint=(0.95, None),
            height=dp(140),
            pos_hint={"center_x": 0.5}
        )

        self.word_label = MDLabel(
            text="...",
            halign="center",
            font_style="H5"
        )

        sub = MDLabel(
            text="Переведите слово",
            halign="center",
            theme_text_color="Secondary"
        )

        self.word_card.add_widget(sub)
        self.word_card.add_widget(self.word_label)
        self.main.add_widget(self.word_card)

        # ANSWERS
        self.buttons_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            size_hint_x=1
        )

        self.buttons_layout.bind(minimum_height=self.buttons_layout.setter("height"))

        self.main.add_widget(self.buttons_layout)

        # MENU
        self.menu_btn = MDRaisedButton(
            text="◀ В меню",
            size_hint_y=None,
            height=dp(50),
            md_bg_color="#9E9E9E",
            on_release=self.exit_to_menu
        )

        self.main.add_widget(self.menu_btn)

        scroll.add_widget(self.main)
        root.add_widget(scroll)
        self.add_widget(root)

    # ================= LOGIC =================

    def on_enter(self):
        self.current_level = getattr(self.manager, 'selected_level', 'marathon')
        self.setup_for_level()
        self.reset_quiz()
        self.load_all_questions()
        Clock.schedule_once(self.load_next_question, 0.2)

    def setup_for_level(self):
        if self.current_level in ("easy", "medium", "hard"):
            self.total_questions = 10
        else:
            self.total_questions = 20

    def reset_quiz(self):
        self.questions_count = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.questions = []
        self.current_question_index = 0
        self.answered = False
        self.waiting_for_next = False
        self.update_progress()

    def update_progress(self):
        progress = (self.questions_count / self.total_questions) * 100 if self.total_questions else 0
        self.progress_bar.value = progress
        self.progress_label.text = f"{self.questions_count}/{self.total_questions}"

    # ================= QUESTIONS =================

    def load_all_questions(self):
        import random

        words = api.get_words()

        if not words:
            show_error("Ошибка загрузки")
            return

        if self.current_level == "marathon":
            filtered = words
        else:
            filtered = [w for w in words if w.get("level") == self.current_level]

        if len(filtered) < 4:
            show_error("Недостаточно слов")
            return

        self.questions = random.sample(filtered, min(len(filtered), self.total_questions))

    # ================= NEXT QUESTION =================

    def load_next_question(self, *args):

        self.answered = False

        if self.current_question_index >= len(self.questions):
            self.show_results()
            return

        self.current_data = self.questions[self.current_question_index]
        self.current_question_index += 1

        self.word_label.text = self.current_data["word"]

        self.buttons_layout.clear_widgets()
        self.current_buttons = []

        correct = self.current_data.get("translation")

        pool = list(set(
            w["translation"] for w in self.questions
            if w.get("translation") != correct
        ))

        import random

        options = [correct]

        while len(options) < 4 and pool:
            opt = random.choice(pool)
            options.append(opt)
            pool.remove(opt)

        while len(options) < 4:
            options.append("—")

        random.shuffle(options)

        # ================= BUTTONS =================
        for opt in options:

            btn = MDRaisedButton(
                size_hint=(1, None),
                md_bg_color=[0.13, 0.59, 0.95, 1]
            )

            label = MDLabel(
                text=opt,
                halign="center",
                valign="middle",
                size_hint=(1, None),
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1]
            )

            def update_text_size(instance, value):
                instance.text_size = (value[0] - dp(20), None)

            label.bind(size=update_text_size)
            label.texture_update()

            btn.height = max(label.texture_size[1] + dp(30), dp(60))

            btn.add_widget(label)

            btn.bind(on_release=lambda instance, value=opt: self.check_answer(instance, value))

            self.buttons_layout.add_widget(btn)
            self.current_buttons.append(btn)

        total_height = sum(btn.height for btn in self.current_buttons) + dp(10) * len(options)
        self.buttons_layout.height = total_height

    # ================= ANSWER =================

    def check_answer(self, btn, selected):

        if self.answered:
            return

        self.answered = True

        correct = self.current_data["translation"]

        api.submit_answer(selected, correct)

        self.questions_count += 1

        if selected == correct:
            self.correct_count += 1
            show_success("Правильно!")
        else:
            self.incorrect_count += 1
            show_error(f"Неверно: {correct}")

        self.update_progress()

        Clock.schedule_once(self.load_next_question, 1.2)

    # ================= RESULT =================

    def show_results(self):

        accuracy = (self.correct_count / self.total_questions) * 100

        def go_levels(*args):
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.manager.current = "level_selection"

        self.dialog = MDDialog(
            title="Результат",
            text=f"Правильных: {self.correct_count}\n"
                 f"Неправильных: {self.incorrect_count}\n"
                 f"Точность: {accuracy:.1f}%",
            buttons=[
                MDRaisedButton(
                    text="К уровням",
                    md_bg_color="#4CAF50",
                    on_release=go_levels
                )
            ],
        )

        self.dialog.open()

    def exit_to_menu(self, *args):
        self.manager.current = "level_selection"