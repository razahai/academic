@echo off

@REM actually commented this file so i would know what i did like 5 years
@REM in the future !!!

set folder=ai
@REM set env variables
for /f "tokens=*" %%v in (%~dp1.env) do set %%v

if not exist %~dp1%folder%\ echo You need to name your AI folder as the following: "%folder%" & exit /b 1

@REM temporarily append -original to the folder so it gets ignored by git
@REM copy the original folder into a new folder called "ai" which will be
@REM committed to the repository
ren %folder% "%folder%-original"
robocopy "%folder%-original" ai /e > nul

cd "./%folder%" || exit /b 1

for /r %%f in (*.py) do (
    @REM get text from file using type cmd and get only the lines that dont 
    @REM match the specified string -> put this into file.txt and then simply
    @REM override the original file 
    (type %%f | findstr /v %NAME%) >> "%%f.txt"
    move /y "%%f.txt" "%%f" > nul
)

cd ..

git add ai > nul

if [%1] == [] (
    git commit -m "routine(ai): update ai folder" > nul
) else (
    git commit -m "routine(ai): %~1" > nul
)

@REM probably bad idea since something could go wrong but who cares
git push origin main

@REM delete the temporary folder and rename the original folder
@REM back to its original name
rd /s /q "./%folder%"
ren "%folder%-original" %folder%