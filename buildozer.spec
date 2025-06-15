[app]

# (str) Title of your application
title = Bbgrams

# (str) Package name
package.name = bbgrams

# (str) Package domain (unique, like a reverse DNS domain)
package.domain = org.example

# (str) Source code directory
source.dir = .

# (str) Main .py file
source.main = main.py

# (str) Application version
version = 0.1

# (list) List of inclusions using pattern matching
source.include_exts = py,png,jpg,kv,atlas

# (list) Permissions
android.permissions = INTERNET

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Application requirements
requirements = python3,kivy

# (str) Entry point for the application
entrypoint = main.py

# (bool) Presplash screen
presplash = images/presplash.png

# (str) Icon of the application
icon.filename = images/icon.png

# (str) Supported Android API
android.api = 33

# (str) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (False = new way, True = legacy)
android.private_storage = False

# (str) Application theme (see https://developer.android.com/guide/topics/ui/look-and-feel/themes)
android.theme = "@android:style/Theme.Material.NoActionBar"

# (list) Patterns to include in APK
android.include_patterns = assets/*,images/*

# (str) Custom source folders for requirements
# (Example: requirements source from a subfolder of your project)
# (Not usually needed)
# requirements.source.kivy = ../../kivy

# (str) Directory with gradle build file
# (default is none)
# android.gradle_path =

# (bool) Copy library instead of using symlink
copy_libs = 1

# (bool) Compile .py to .pyo (optimized bytecode)
# (deprecated, no longer used)
# optimize = 1

# (str) Custom command to run at build time
# build.cmd = echo "Custom build step"

# (str) Custom command to run before packaging
# prebuild.cmd =

# (str) Custom command to run after packaging
# postbuild.cmd =

# (bool) Enable android archs
android.archs = armeabi-v7a, arm64-v8a

# (str) Path to keystore
# android.keystore = my.keystore
# android.keyalias = mykey
# android.keyalias_password = mypassword
# android.keystore_password = mypassword
