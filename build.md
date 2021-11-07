# Notes on the build process

Run PyInstaller in the project root directory, not `app` (since we want PyInstaller to create `build` and `dist` directories there).

To build server, use:
```
$ pyinstaller --noconsole --name server app\server\main.py
```

To build client:
```
$ pyinstaller --noconsole --name client app\client\main.py
```

Since client needs to load `.ui` and image files, copy the directory `app\client\ui` into `dist\client`.
