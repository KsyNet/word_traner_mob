from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from mobile_app.api_client import register


class RegisterScreen(MDScreen):

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
            height=360,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=10,
            radius=[20, 20, 20, 20]
        )

        title = MDLabel(
            text="🆕 Регистрация",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        subtitle = MDLabel(
            text="Создайте новый аккаунт",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )

        self.username = MDTextField(
            hint_text="Логин",
            mode="rectangle",
            icon_left="account"
        )

        self.password = MDTextField(
            hint_text="Пароль",
            password=True,
            mode="rectangle",
            icon_left="lock"
        )

        btn = MDRaisedButton(
            text="ЗАРЕГИСТРИРОВАТЬСЯ",
            md_bg_color="#4CAF50",
            size_hint_y=None,
            height=50,
            on_release=self.do_register
        )

        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.username)
        card.add_widget(self.password)
        card.add_widget(btn)

        root.add_widget(card)
        self.add_widget(root)

    def do_register(self, _):
        register(self.username.text, self.password.text)
        self.manager.current = "login"