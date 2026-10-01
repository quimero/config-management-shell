@echo off
pushd "%~dp0.."

call run.bat --vfs tests\vfs\minimal --script tests\start_ok.txt

if errorlevel 1 (
    echo TEST FAILED
    popd
    exit /b 1
)

echo TEST PASSED
popd
