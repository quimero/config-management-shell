@echo off
pushd "%~dp0.."

echo Testing minimal VFS...
call run.bat --vfs tests\vfs\minimal --script tests\stage3_minimal.txt

if errorlevel 1 goto fail

echo TEST PASSED
popd
exit /b 0

:fail
echo TEST FAILED
popd
exit /b 1
