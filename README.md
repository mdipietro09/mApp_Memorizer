# Kivy App for Memorizing stuff

#### Setup for iOS deployment
```
brew install autoconf automake libtool pkg-config
brew link libtool
pip install Cython
pip install kivy-ios
```
now toolchain command
```
toolchain build kivy (...30 min)
toolchain create mappmemo ~/some/path/directory
open mappmemo-ios/mappmemo.xcodeproj
```

build button fail, retry, ...
ModuleNotFoundError: No module named 'kivymd'
```
toolchain build pillow
toolchain pip install kivymd
toolchain update mappmemo-ios/mappmemo.xcodeproj
```

if don't see icons:
	env.../site-packages/kivy_ios/recipes/sdl2_ttf/__init__.py
	version = "2.0.15"
```
toolchain clean sdl2_ttf
toolchain build sdl2_ttf
```