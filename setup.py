import os
import subprocess
import sys
import ctypes
import shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def get_python_versions():
    python_versions = {}
    counter = 0
    for python_exe in subprocess.check_output(['where', 'python']).decode().splitlines():
        if 'WindowsApps' in python_exe:
            for root, dirs, files in os.walk(os.environ['USERPROFILE']):
                for file in files:
                    if file == 'python.exe':
                        python_exe = os.path.join(root, file)
                        break
        python_version = subprocess.check_output([python_exe, '--version']).decode().splitlines()[0].split()[1]
        if python_exe not in python_versions:
            counter += 1
            python_versions[counter] = {'version': python_version, 'path': python_exe}
            print(f"{counter}. Found Python version {python_version}: {python_exe}")
    return python_versions

def create_virtual_environment(python_path, version):
    temp_dir = os.path.join(os.environ['TEMP'], f"venv_{version}")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
    venv_name = os.path.join(temp_dir, f".venv_{version}")
    print(f"Creating Virtual Environment for Python version {version}...")
    subprocess.run([python_path, '-m', 'venv', venv_name])
    return venv_name

def install_requirements(venv_name):
    script_dir = os.path.dirname(__file__)
    requirements_file = os.path.join(script_dir, 'requirements.txt')
    print("Installing Requirements...")
    subprocess.run([f"{venv_name}\\Scripts\\pip", 'install', '-r', requirements_file])

def main():
    run_as_admin()
    if is_admin():
        print("Running as admin")
    else:
        print("Not running as admin")
        sys.exit(1)

    python_versions = get_python_versions()
    if not python_versions:
        print("No Python installations found in PATH. Please install Python and try again.")
        sys.exit(1)

    selected_number = input("Enter the left number of the desired Python version from the list above: ")
    if int(selected_number) not in python_versions:
        print("Invalid selection! Exiting...")
        sys.exit(1)

    selected_version = python_versions[int(selected_number)]['version']
    selected_python_path = python_versions[int(selected_number)]['path']

    venv_name = create_virtual_environment(selected_python_path, selected_version)
    install_requirements(venv_name)

    script_dir = os.path.dirname(__file__)
    builder_file = os.path.join(script_dir, 'builder.py')
    if subprocess.run([f"{venv_name}\\Scripts\\python", builder_file]).returncode == 0:
        print("Setup Complete!")
    else:
        print("Setup Failed!")
        print("Check the error message above.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
