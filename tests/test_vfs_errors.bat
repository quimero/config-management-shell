@echo off
pushd "%~dp0.."

echo Test 1: Missing VFS
call run.bat --vfs tests\vfs\missing --script tests\stage3_minimal.txt
if not errorlevel 1 goto fail

echo Test 2: File instead of directory
call run.bat --vfs tests\vfs\minimal\hello.txt
if not errorlevel 1 goto fail

echo Test 3: Unknown command
call run.bat --vfs tests\vfs\multiple --script tests\start_error.txt
if not errorlevel 1 goto fail

echo Test 4: Invalid arguments
call run.bat --vfs tests\vfs\minimal --script tests\stage3_bad_args.txt
if not errorlevel 1 goto fail

echo ALL ERROR TESTS PASSED
popd
exit /b 0

:fail
echo TEST FAILED
popd
exit /b 1
