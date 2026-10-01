@echo off
pushd "%~dp0.."

echo Testing multiple files VFS...
call run.bat --vfs tests\vfs\multiple --script tests\stage3_multiple.txt

if errorlevel 1 goto fail

echo TEST PASSED
popd
exit /b 0

:fail
echo TEST FAILED
popd
exit /b 1
