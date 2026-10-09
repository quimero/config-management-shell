@echo off
pushd "%~dp0.."

echo Testing stage 5 successful commands...
call run.bat --vfs tests\vfs\multiple --script tests\stage5_success.txt

if errorlevel 1 goto fail

echo.
echo Testing stage 5 error handling...
call run.bat --vfs tests\vfs\multiple --script tests\stage5_errors.txt

if not errorlevel 1 goto fail

echo.
echo STAGE 5 TESTS PASSED
popd
exit /b 0

:fail
echo.
echo STAGE 5 TEST FAILED
popd
exit /b 1