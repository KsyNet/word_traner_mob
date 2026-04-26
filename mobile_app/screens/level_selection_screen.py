from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_info


class LevelSelectionScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20
        )

        card = MDCard(
            orientation="vertical",
            padding=25,
            spacing=15,
            size_hint=(0.9, None),
            height=450,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=10,
            radius=[20, 20, 20, 20]
        )

        title = MDLabel(
            text="🎯 Выбор уровня",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        subtitle = MDLabel(
            text="Выберите сложность викторины",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )

        btn_easy = MDRaisedButton(
            text="🟢 Лёгкий (10 вопросов)",
            md_bg_color="#4CAF50",
            size_hint_y=None,
            height=50,
            on_release=lambda x: self.start("easy")
        )

        btn_medium = MDRaisedButton(
            text="🟡 Средний (10 вопросов)",
            md_bg_color="#FF9800",
            size_hint_y=None,
            height=50,
            on_release=lambda x: self.start("medium")
        )

        btn_hard = MDRaisedButton(
            text="🔴 Сложный (10 вопросов)",
            md_bg_color="#F44336",
            size_hint_y=None,
            height=50,
            on_release=lambda x: self.start("hard")
        )

        btn_marathon = MDRaisedButton(
            text="🏆 Марафон (20 вопросов)",
            md_bg_color="#3F51B5",
            size_hint_y=None,
            height=50,
            on_release=lambda x: self.start("marathon")
        )

        back_btn = MDRaisedButton(
            text="НАЗАД",
            md_bg_color="#9E9E9E",
            size_hint_y=None,
            height=45,
            on_release=lambda x: self.go_back()
        )

        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(btn_easy)
        card.add_widget(btn_medium)
        card.add_widget(btn_hard)
        card.add_widget(btn_marathon)
        card.add_widget(back_btn)

        root.add_widget(card)
        self.add_widget(root)

    def start(self, level):
        words = api.get_words()

        if not words or len(words) < 4:
            show_error("Недостаточно слов для викторины! Добавьте минимум 4 слова.")
            return

        if level != "marathon":
            level_words = [w for w in words if w.get('level', 'easy') == level]
            if len(level_words) < 4:
                show_error(f"Недостаточно слов уровня {level}! Добавьте минимум 4 слова этого уровня.")
                return

        show_info(f"Запуск {self.get_level_name(level)}...")
        self.manager.selected_level = level
        self.manager.current = "quiz"

    def get_level_name(self, level):
        names = {
            "easy": "лёгкого уровня",
            "medium": "среднего уровня",
            "hard": "сложного уровня",
            "marathon": "марафона"
        }
        return names.get(level, "викторины")

    def go_back(self):
        self.manager.current = "menu"