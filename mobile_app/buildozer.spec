[app]
title = WordTrainer
package.name = wordtrainer
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 1.0

requirements = python3,kivy,kivymd,requests

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b

# важно для KivyMD
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1