from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_success, show_info


class DeleteWordScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(orientation="vertical", padding=20, spacing=10)

        # ===== HEADER FILTER PANEL =====
        self.filter_level = "all"

        filter_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=10
        )

        self.filter_btn = MDRaisedButton(
            text="Фильтр: Все",
            md_bg_color="#607D8B",
            on_release=self.open_filter_menu
        )

        sort_btn = MDRaisedButton(
            text="A-Z",
            md_bg_color="#3F51B5",
            on_release=self.toggle_sort
        )

        self.sort_az = True

        filter_box.add_widget(self.filter_btn)
        filter_box.add_widget(sort_btn)

        # ===== LIST =====
        self.scroll = MDScrollView()
        self.list = MDList()
        self.scroll.add_widget(self.list)

        # ===== BACK BUTTON =====
        back_btn = MDRaisedButton(
            text="Назад",
            size_hint_y=None,
            height=50,
            md_bg_color="#9E9E9E",
            on_release=self.back
        )

        root.add_widget(filter_box)
        root.add_widget(self.scroll)
        root.add_widget(back_btn)

        self.add_widget(root)

        self.dialog = None
        self.all_words = []

    def on_enter(self):
        self.load_words()

    # ================= LOAD =================
    def load_words(self):
        self.list.clear_widgets()
        words = api.get_words()

        if not words or isinstance(words, dict) and words.get("error"):
            self.list.add_widget(
                MDLabel(text="Нет слов", halign="center")
            )
            return

        self.all_words = words
        self.render_words()

    # ================= RENDER =================
    def render_words(self):
        self.list.clear_widgets()

        words = self.all_words

        # FILTER
        if self.filter_level != "all":
            words = [w for w in words if w.get("level", "easy") == self.filter_level]

        # SORT
        words = sorted(
            words,
            key=lambda x: x["word"].strip().lower(),
            reverse=not self.sort_az
        )

        if not words:
            self.list.add_widget(
                MDLabel(text="Нет слов по фильтру", halign="center")
            )
            return

        show_info(f"Загружено {len(words)} слов")

        for w in words:
            item = ThreeLineListItem(
                text=w['word'],
                secondary_text=w['translation'],
                tertiary_text=f"Уровень: {w.get('level', 'easy')}"
            )
            item.word_data = w
            item.bind(on_release=self.confirm_delete)
            self.list.add_widget(item)

    # ================= FILTER MENU =================
    def open_filter_menu(self, btn):
        items = [
            {"viewclass": "OneLineListItem", "text": "Все",
             "on_release": lambda: self.set_filter("all", "Все")},
            {"viewclass": "OneLineListItem", "text": "Easy",
             "on_release": lambda: self.set_filter("easy", "Easy")},
            {"viewclass": "OneLineListItem", "text": "Medium",
             "on_release": lambda: self.set_filter("medium", "Medium")},
            {"viewclass": "OneLineListItem", "text": "Hard",
             "on_release": lambda: self.set_filter("hard", "Hard")},
        ]

        self.menu = MDDropdownMenu(caller=btn, items=items, width_mult=4)
        self.menu.open()

    def set_filter(self, level, text):
        self.filter_level = level
        self.filter_btn.text = f"Фильтр: {text}"
        self.menu.dismiss()
        self.render_words()

    # ================= SORT =================
    def toggle_sort(self, btn):
        self.sort_az = not self.sort_az
        btn.text = "A-Z" if self.sort_az else "Z-A"
        self.render_words()

    # ================= DELETE =================
    def confirm_delete(self, item):
        self.selected = item.word_data

        self.dialog = MDDialog(
            title="Удаление слова",
            text=f"Удалить?\n\n{self.selected['word']} - {self.selected['translation']}",
            buttons=[
                MDRaisedButton(text="Отмена", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Удалить", md_bg_color="#F44336", on_release=self.delete_word)
            ]
        )
        self.dialog.open()

    def delete_word(self, *args):
        result = api.delete_word(self.selected["id"])
        self.dialog.dismiss()

        if result.get("ok"):
            show_success(f"Удалено: {self.selected['word']}")
            self.load_words()
        else:
            show_error("Ошибка удаления")

    # ================= NAV =================
    def back(self, *args):
        self.manager.current = "menu"