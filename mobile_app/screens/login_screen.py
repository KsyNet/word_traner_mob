from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

import mobile_app.api_client as api
from mobile_app.utils import show_error, show_success, show_dialog


class LoginScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=25,
            adaptive_height=True
        )

        # Карточка формы
        card = MDCard(
            orientation="vertical",
            padding=30,
            spacing=20,
            size_hint=(0.9, None),
            height=380,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=10,
            radius=[20, 20, 20, 20]
        )

        # Заголовок
        title = MDLabel(
            text="🔐 Вход в систему",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        subtitle = MDLabel(
            text="Введите данные для входа",
            halign="center",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )

        self.u = MDTextField(
            hint_text="Логин",
            mode="rectangle",
            icon_left="account"
        )

        self.p = MDTextField(
            hint_text="Пароль",
            password=True,
            mode="rectangle",
            icon_left="lock"
        )

        btn_login = MDRaisedButton(
            text="ВОЙТИ",
            md_bg_color="#2196F3",
            size_hint_y=None,
            height=50,
            on_release=self.do_login
        )

        btn_register = MDRaisedButton(
            text="РЕГИСТРАЦИЯ",
            md_bg_color="#4CAF50",
            size_hint_y=None,
            height=50,
            on_release=self.do_register
        )

        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.u)
        card.add_widget(self.p)
        card.add_widget(btn_login)
        card.add_widget(btn_register)

        root.add_widget(card)
        self.add_widget(root)

    def do_login(self, *args):
        if not self.u.text or not self.p.text:
            show_error("Заполните логин и пароль")
            return

        r = api.login(self.u.text, self.p.text)
        if r.get("ok"):
            show_success(f"Добро пожаловать, {self.u.text}!")
            self.manager.current = "menu"
        else:
            show_error("Неверный логин или пароль")

    def do_register(self, *args):
        if not self.u.text or not self.p.text:
            show_error("Введите логин и пароль")
            return

        if len(self.p.text) < 3:
            show_error("Пароль должен быть не менее 3 символов")
            return

        r = api.register(self.u.text, self.p.text)
        if r.get("ok"):
            show_success("Регистрация успешна!")
            self.manager.current = "menu"
        else:
            show_error(r.get("error", "Ошибка регистрации"))