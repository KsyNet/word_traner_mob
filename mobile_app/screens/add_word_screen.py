from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_success, show_info


class AddWordScreen(MDScreen):

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
            text="➕ Добавить новое слово",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        subtitle = MDLabel(
            text="Пополняйте свой словарь",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )

        self.word = MDTextField(
            hint_text="Слово",
            mode="rectangle",
            icon_left="book"
        )

        self.translation = MDTextField(
            hint_text="Перевод",
            mode="rectangle",
            icon_left="translate"
        )

        self.level_btn = MDRaisedButton(
            text="Уровень: Easy",
            md_bg_color="#4CAF50",
            size_hint_y=None,
            height=45
        )

        self.level_btn.bind(on_release=self.open_menu)

        save_btn = MDRaisedButton(
            text="СОХРАНИТЬ",
            md_bg_color="#2196F3",
            size_hint_y=None,
            height=50,
            on_release=self.save
        )

        back_btn = MDRaisedButton(
            text="НАЗАД",
            md_bg_color="#9E9E9E",
            size_hint_y=None,
            height=45,
            on_release=self.back
        )

        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.word)
        card.add_widget(self.translation)
        card.add_widget(self.level_btn)
        card.add_widget(save_btn)
        card.add_widget(back_btn)

        root.add_widget(card)
        self.add_widget(root)

        self.selected_level = "easy"
        self.level_menu = None

    def open_menu(self, btn):
        items = [
            {"viewclass": "OneLineListItem", "text": "Easy",
             "on_release": lambda: self.set_level("easy", "Easy", "#4CAF50")},
            {"viewclass": "OneLineListItem", "text": "Medium",
             "on_release": lambda: self.set_level("medium", "Medium", "#FF9800")},
            {"viewclass": "OneLineListItem", "text": "Hard",
             "on_release": lambda: self.set_level("hard", "Hard", "#F44336")},
        ]
        self.level_menu = MDDropdownMenu(caller=btn, items=items, width_mult=3)
        self.level_menu.open()

    def set_level(self, level, text, color):
        self.selected_level = level
        self.level_btn.text = f"Уровень: {text}"
        self.level_btn.md_bg_color = color
        self.level_menu.dismiss()
        show_info(f"Выбран уровень: {text}")

    def save(self, *args):
        word = self.word.text.strip()
        translation = self.translation.text.strip()

        if not word:
            show_error("Введите слово")
            return

        if not translation:
            show_error("Введите перевод")
            return

        result = api.add_word(word, translation, self.selected_level)

        if result.get("ok"):
            show_success(f"Слово '{word}' добавлено!")
            self.word.text = ""
            self.translation.text = ""
        else:
            show_error("Ошибка при добавлении слова")

    def back(self, *args):
        if self.word.text or self.translation.text:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDRaisedButton

            dialog = MDDialog(
                title="Несохраненные изменения",
                text="Вы действительно хотите выйти? Введенные данные будут потеряны.",
                buttons=[
                    MDRaisedButton(text="Нет", on_release=lambda x: dialog.dismiss()),
                    MDRaisedButton(
                        text="Да",
                        on_release=lambda x: (
                            dialog.dismiss(),
                            setattr(self.manager, 'current', 'menu')
                        )
                    )
                ]
            )
            dialog.open()
        else:
            self.manager.current = "menu"