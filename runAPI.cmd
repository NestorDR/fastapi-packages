@echo off
cls

rem Set environment
call env\Scripts\deactivate.bat
call env\Scripts\activate.bat

rem Run API
set FASTAPI_PACKAGES_DB_ENGINE=SQLite
rem set FASTAPI_PACKAGES_DB_ENGINE=PostgreSQL
set FASTAPI_SIMPLE_SECURITY_SECRET=8df2b351-59a0-4b5c-a85b-fd59a5db28a8
set FASTAPI_SIMPLE_SECURITY_HIDE_DOCS=
uvicorn --port 8000 --host 127.0.0.1 app.main:app --reload
set FASTAPI_PACKAGES_DB_ENGINE=
set FASTAPI_SIMPLE_SECURITY_SECRET=
set FASTAPI_SIMPLE_SECURITY_HIDE_DOCS=
