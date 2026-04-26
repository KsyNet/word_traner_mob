from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_info


class StatsScreen(MDScreen):

    def on_enter(self):
        self.load()

    def load(self):
        self.clear_widgets()

        s = api.stats()

        if s.get("error"):
            show_error("Не удалось загрузить статистику")
            return

        total = s.get('correct_answers', 0) + s.get('incorrect_answers', 0)
        accuracy = (s.get('correct_answers', 0) / total * 100) if total > 0 else 0

        root = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20
        )

        card = MDCard(
            orientation="vertical",
            padding=25,
            spacing=15,
            size_hint=(0.95, None),
            height=420,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=10,
            radius=[20, 20, 20, 20]
        )

        title = MDLabel(
            text="📊 Статистика",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        text = f"""
📚 Слов в словаре: {s.get('word_count', 0)}

✅ Правильных: {s.get('correct_answers', 0)}
❌ Неправильных: {s.get('incorrect_answers', 0)}

📈 Всего попыток: {total}
🎯 Точность: {accuracy:.1f}%
        """

        stats_label = MDLabel(
            text=text,
            halign="center",
            font_style="Body1"
        )

        btn = MDRaisedButton(
            text="НАЗАД",
            md_bg_color="#2196F3",
            size_hint_y=None,
            height=50,
            on_release=self.back
        )

        card.add_widget(title)
        card.add_widget(stats_label)
        card.add_widget(btn)

        root.add_widget(card)
        self.add_widget(root)

        if total > 0:
            show_info(f"Точность: {accuracy:.1f}%")

    def back(self, *args):
        self.manager.current = "menu"