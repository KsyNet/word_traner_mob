from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

import mobile_app.api_client as api


class MainMenu(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        # ===== HEADER CARD =====
        header = MDCard(
            orientation="vertical",
            padding=25,
            size_hint=(0.95, None),
            height=160,
            pos_hint={"center_x": 0.5},
            elevation=10,
            radius=[20, 20, 20, 20],
            md_bg_color="#2196F3"
        )

        self.username_label = MDLabel(
            text="👋 Привет!",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )

        header.add_widget(self.username_label)

        header.add_widget(MDLabel(
            text="Выберите действие",
            halign="center",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.9]
        ))

        root.add_widget(header)

        # ===== BUTTONS CARD =====
        buttons_box = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            padding=10
        )

        buttons = [
            ("📝 Добавить слово", "add", "#4CAF50"),
            ("🗑️ Удалить слово", "delete", "#F44336"),
            ("🎯 Викторина", "level_selection", "#FF9800"),
            ("📊 Статистика", "stats", "#2196F3"),
        ]

        for text, screen, color in buttons:
            btn = MDRaisedButton(
                text=text,
                size_hint_y=None,
                height=55,
                md_bg_color=color
            )
            btn.bind(on_release=lambda x, s=screen: self.go_to(s))
            buttons_box.add_widget(btn)

        # ===== LOGOUT =====
        logout_btn = MDRaisedButton(
            text="🚪 Выйти из аккаунта",
            size_hint_y=None,
            height=50,
            md_bg_color="#9E9E9E"
        )
        logout_btn.bind(on_release=self.logout)

        buttons_box.add_widget(logout_btn)

        root.add_widget(buttons_box)
        self.add_widget(root)

    def go_to(self, screen_name):
        self.manager.current = screen_name

    def logout(self, instance):
        api.USER_ID = None
        api.USERNAME = None
        self.manager.current = "login"

    def on_enter(self):
        username = api.get_username()

        if username:
            self.username_label.text = f"👋 Привет, {username}!"
        else:
            self.username_label.text = "👋 Привет!"