@echo off
cls

rem Run a container based on image
docker run -d --name ndr_fastapi_packages -p 80:80 ndr_fastapi_packages_image

