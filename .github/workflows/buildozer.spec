[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = Bananagrams
package.name = bananagrams
package.domain = org.example
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait

# Optional: deine main.py Datei
source.dir = .

# Android spezifisch
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.arch = armeabi-v7a

[buildozer]
