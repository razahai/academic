@echo off

set folder=ai
@REM set env variables
for /f "tokens=*" %%v in (%CD%\.env) do set %%v

if not exist %CD%\courses\tjhsst\%folder%\ echo You need to name your AI folder as the following: "%folder%" & exit /b 1

@REM temporarily append -original to the folder so it gets ignored by git
@REM copy the original folder into a new folder called "ai" which will be
@REM committed to the repository
ren "courses\tjhsst\%folder%" "%folder%-original"
robocopy "courses\tjhsst\%folder%-original" courses\tjhsst\ai /E > nul

cd "./courses/tjhsst/%folder%" || exit /b 1

for /r %%f in (*.py) do (
    @REM get text from file using type cmd and get only the lines that dont 
    @REM match the specified string -> put this into <file>.txt and then simply
    @REM override the original file 
    (type %%f | findstr /v %NAME%) >> "%%f.txt"
    move /y "%%f.txt" "%%f" > nul
)

cd ../../..

git add courses/tjhsst/ai > nul

if [%1] == [] (
    git commit -m "update ai folder" > nul
) else (
    git commit -m "%~1" > nul
)

git push origin main

@REM delete the temporary folder and rename the original folder
@REM back to its original name
rd /s /q "./courses/tjhsst/%folder%"
ren "courses\tjhsst\%folder%-original" %folder%