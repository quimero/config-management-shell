@echo off
pushd "%~dp0.."

echo Testing nested VFS...
call run.bat --vfs tests\vfs\nested --script tests\stage3_nested.txt

if errorlevel 1 goto fail

echo TEST PASSED
popd
exit /b 0

:fail
echo TEST FAILED
popd
exit /b 1
