@echo off
cls

rem Set environment
call env\Scripts\deactivate.bat
call env\Scripts\activate.bat

rem Identify if user wants to production context using the command line argument
set FASTAPI_PACKAGES_PORT=8000
if /i [%~1]==[P] set FASTAPI_PACKAGES_PORT=80

rem Run stub
:run
py test/stub_DA.py -U http://127.0.0.1:%FASTAPI_PACKAGES_PORT%/ -K fbd1d865-9ae8-491f-98b8-1f522c52eb02
set FASTAPI_PACKAGES_PORT=