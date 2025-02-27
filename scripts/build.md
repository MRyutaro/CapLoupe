```
del CapLoupe.spec
rd /s /q build dist output
pyinstaller --onefile --noconsole CapLoupe.py
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```
