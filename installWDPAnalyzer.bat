@echo off
setlocal

set "vbscript=%temp%\folderdialog.vbs"
set "download_path="

:: Create a temporary VBScript file
echo Set objShell = WScript.CreateObject("Shell.Application") > "%vbscript%"
echo Set objFolder = objShell.BrowseForFolder(0, "Select the path to download the Wildlife Dimension Probe Analyzer files:", 0, 0) >> "%vbscript%"
echo If objFolder Is Nothing Then >> "%vbscript%"
echo     WScript.Quit(1) >> "%vbscript%"
echo End If >> "%vbscript%"
echo WScript.Echo objFolder.Self.Path >> "%vbscript%"

:: Execute the VBScript and capture the selected directory path
for /f "delims=" %%I in ('cscript //nologo "%vbscript%"') do set "download_path=%%I"

:: Remove the temporary VBScript file
del "%vbscript%"

if "%download_path%"=="" (
    echo No directory path selected. Exiting script.
    pause
    exit /b
)

echo Downloading Python files...
curl -L -o "%download_path%\control.py" "https://raw.githubusercontent.com/gageisokV2/Wildlife_Dimensional_probe_analyzer/main/control.py"
curl -L -o "%download_path%\plotter.py" "https://raw.githubusercontent.com/gageisokV2/Wildlife_Dimensional_probe_analyzer/main/plotter.py"

echo Python files downloaded successfully to %download_path%.

:: Install required Python libraries using pip
echo Installing required Python libraries...
pip install pyvista
pip install numpy

:: Create a launcher batch file
set "launcher_path=%download_path%\launch_control.bat"

echo @echo off > "%launcher_path%"
echo cd /d "%download_path%" >> "%launcher_path%"
echo python control.py >> "%launcher_path%"

echo Launcher batch file created successfully.
echo Copy and paste the launch_control.bat file into an easily accessed place (such as a desktop) to quickly launch the program

pause
