@echo off
pushd "%~dp0.."

echo Testing stage 4 successful commands...
call run.bat --vfs tests\vfs\multiple --script tests\stage4_success.txt

if errorlevel 1 goto fail

echo.
echo Testing stage 4 error handling...
call run.bat --vfs tests\vfs\multiple --script tests\stage4_errors.txt

if not errorlevel 1 goto fail

echo.
echo STAGE 4 TESTS PASSED
popd
exit /b 0

:fail
echo.
echo STAGE 4 TEST FAILED
popd
exit /b 1