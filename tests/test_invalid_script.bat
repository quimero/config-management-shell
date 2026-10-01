@echo off
pushd "%~dp0.."

call run.bat --script tests\missing.txt

if errorlevel 1 (
    echo TEST PASSED
    popd
    exit /b 0
)

echo TEST FAILED
popd
exit /b 1
