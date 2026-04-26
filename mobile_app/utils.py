from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.window import Window


class Notification(MDCard):
    """Всплывающее уведомление"""

    def __init__(self, text, type="info", duration=2, **kwargs):
        super().__init__(**kwargs)

        colors = {
            "success": [0.3, 0.7, 0.3, 0.95],
            "error": [0.9, 0.3, 0.3, 0.95],
            "info": [0.3, 0.5, 0.8, 0.95]
        }

        icons = {
            "success": "✅ ",
            "error": "❌ ",
            "info": "ℹ️ "
        }

        self.size_hint = (0.85, None)
        self.height = 60
        self.pos_hint = {"center_x": 0.5, "top": 1}
        self.elevation = 6
        self.radius = [16, 16, 16, 16]
        self.md_bg_color = colors.get(type, colors["info"])

        label = MDLabel(
            text=f"{icons.get(type, '')}{text}",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )
        label.bind(size=label.setter('text_size'))

        self.add_widget(label)

        Clock.schedule_once(self.remove_self, duration)

    def remove_self(self, dt):
        if self.parent:
            self.parent.remove_widget(self)


class Toast:
    """Упрощённые уведомления"""

    _toast = None

    @classmethod
    def show(cls, text, duration=2, type="info"):

        colors = {
            "success": [0.3, 0.7, 0.3, 0.95],
            "error": [0.9, 0.3, 0.3, 0.95],
            "info": [0.3, 0.5, 0.8, 0.95]
        }

        icons = {
            "success": "✅ ",
            "error": "❌ ",
            "info": "ℹ️ "
        }

        # удалить старый toast
        if cls._toast and cls._toast.parent:
            cls._toast.parent.remove_widget(cls._toast)

        cls._toast = MDCard(
            size_hint=(0.9, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.02},
            elevation=10,
            radius=[15, 15, 15, 15],
            md_bg_color=colors.get(type, colors["info"])
        )

        label = MDLabel(
            text=f"{icons.get(type, '')}{text}",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        label.bind(size=label.setter('text_size'))

        cls._toast.add_widget(label)

        Window.add_widget(cls._toast)

        Clock.schedule_once(cls.hide, duration)

    @classmethod
    def hide(cls, dt):
        if cls._toast and cls._toast.parent:
            cls._toast.parent.remove_widget(cls._toast)
            cls._toast = None


def show_error(message):
    Toast.show(message, 3, "error")


def show_success(message):
    Toast.show(message, 2, "success")


def show_info(message):
    Toast.show(message, 2, "info")


def show_dialog(title, text, callback=None):
    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=lambda x: (
                    dialog.dismiss(),
                    callback() if callback else None
                )
            )
        ]
    )
    dialog.open()
    return dialog