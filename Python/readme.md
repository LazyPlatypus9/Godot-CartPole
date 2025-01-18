# Windows
If running manually, you will need to change the execution protocol to start the virtual environment on Windows. Run `Set-ExecutionPolicy Unrestricted -Scope Process` in the VS Code terminal before proceeding. **This step will need to be repeated each time VS Code is opened, setting the execution process globally is a security risk.**

I would suggest using the `build_python_windows.sh` script in the root directory as it doesn't require the ExecutionPolicy to change.

# Virtual Environment
1. Run `./build.sh`
2. Depending on whether you are on Linux or Windows, the command diverges
    * On Linux, run `./activate.sh`
    * On Windows, first change the ExecutionPolicy, then run `.virtual/Scripts/activate`
3. Run `./packages.sh`