# Kivy App for Memorizing stuff

### Setup for iOS deployment
```
brew install autoconf automake libtool pkg-config
brew link libtool
pip install Cython
pip install kivy-ios
```
now use toolchain command:
```
toolchain build kivy (...30 min)
toolchain create mappmemo ~/some/path/directory
open mappmemo-ios/mappmemo.xcodeproj
```
Xcode opens:
- change "Display Name"
- select "Requires full screen"
- upload and select the App Icons

<br/>
Push build button (if fail, retry to push)

<br/> 
**If you get pkg error like:**
<br/>&nbsp;&nbsp;&nbsp; *ModuleNotFoundError: No module named 'kivymd'*

```
toolchain build pillow
toolchain pip install kivymd
toolchain update mappmemo-ios/mappmemo.xcodeproj
```

<br/>
**If when simulator is running don't see icons:**
<br/>&nbsp;&nbsp;&nbsp; go to env.../site-packages/kivy_ios/recipes/sdl2_ttf/__init__.py
<br/>&nbsp;&nbsp;&nbsp; change version to 2.0.15

```
version = "2.0.15"
```
<br/>&nbsp;&nbsp;&nbsp; then run
```
toolchain clean sdl2_ttf
toolchain build sdl2_ttf
```