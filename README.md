# PayTrack
PayTrack provides a GUI for AMCAIM staff that allows easy creation of payment invoices.

## Usage
- download the latest build.
- unzip the contents.
- run the executable.

## Build using script (recommended):
### Run `builder.py` with optional flags:
- no flags will build the exe with the next minor build number.
- `--no-selector` to skip version selector and automatically build using the next minor build number.
- `--deps` to install dependencies.

## Build manually:
1. run ```pip install CTkMessagebox pyinstaller customtkinter docx2pdf python-docx python-dateutil``` 
2. run ```python -m PyInstaller main.py --onefile -w --icon=assets\icons\logo.ico --name="PayTrack"```
