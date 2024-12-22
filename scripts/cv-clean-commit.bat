@echo off

set folder=cv
@REM set env variables
for /f "tokens=*" %%v in (%CD%\.env) do set %%v

if not exist %CD%\courses\tjhsst\%folder%\ echo You need to name your CV folder as the following: "%folder%" & exit /b 1

@REM temporarily append -original to the folder so it gets ignored by git
@REM copy the original folder into a new folder called "cv" which will be
@REM committed to the repository
ren courses\tjhsst\%folder% "courses\tjhsst\%folder%-original"
robocopy "courses\tjhsst\%folder%-original" courses\tjhsst\cv /E > nul

cd "./courses/tjhsst/%folder%" || exit /b 1

setlocal enabledelayedexpansion

for /r %%f in (*) do (
    (for /f "delims=" %%l in ('findstr /n "^" "%%f"') do (
        set "line=%%l"
        setlocal enabledelayedexpansion
        set "line=!line:*:=!"
        if defined line (
            set "line=!line:%ION_USERNAME%=--!"
        )
        if defined line (
            echo(!line!
        ) else (
            echo.
        )
        endlocal
    )) > "%%f.txt"
    move /y "%%f.txt" "%%f" > nul
)

endlocal

cd ..

git add courses/tjhsst/cv > nul

if [%1] == [] (
    git commit -m "update cv folder" > nul
) else (
    git commit -m "%~1" > nul
)

git push origin main

@REM delete the temporary folder and rename the original folder
@REM back to its original name
rd /s /q "./courses/tjhsst/%folder%"
ren "courses\tjhsst\%folder%-original" courses\tjhsst\%folder%