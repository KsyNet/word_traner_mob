import os
import sys

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# стабильный импорт проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# фикс размера (для Android и теста на ПК)
Window.size = (360, 640)

from screens.login_screen import LoginScreen
from screens.main_menu import MainMenu
from screens.add_word_screen import AddWordScreen
from screens.delete_word_screen import DeleteWordScreen
from screens.quiz_screen import QuizScreen
from screens.stats_screen import StatsScreen
from screens.level_selection_screen import LevelSelectionScreen

import api_client as api


class WordTrainerApp(MDApp):

    def build(self):
        self.title = "Word Trainer"

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()

        screens = [
            LoginScreen(name="login"),
            MainMenu(name="menu"),
            AddWordScreen(name="add"),
            DeleteWordScreen(name="delete"),
            QuizScreen(name="quiz"),
            StatsScreen(name="stats"),
            LevelSelectionScreen(name="level_selection"),
        ]

        for screen in screens:
            sm.add_widget(screen)

        sm.current = "login"
        return sm


if __name__ == "__main__":
    WordTrainerApp().run()