rem %1 - Drive where venv will be
rem %2 - Addon folder
rem %3 - Path Venv

echo param 1 = %1
echo param 2 = %2
echo param 3 = %3
echo param_custom_env_folder3 = %4

%1:
if exist %3\py310\ (
  echo Yes 
  echo create venv
  cd %3\py310\
  python -m virtualenv %3\%4
) else (
  echo No
  echo copy python 3.10 files
  xcopy %2\python_3.10 %3\\py310\ /e
  echo create venv
  
  @REM cd %3\py39\
  @REM python -m virtualenv %3\sd_env
  echo if it doenst work, run this manually
  echo %3\py310\python.exe -m virtualenv %3\%4
  %3\py310\python.exe -m virtualenv %3\%4
  
)
@REM echo git packages compiled
@REM xcopy %2\site-packages %3\\%4\Lib\site-packages\ /e
@REM xcopy %2\src %3\\%4\src\ /e