#!/usr/bin/env python3
import os
import shutil
import subprocess
import platform
from pathlib import Path

def is_ec2():
    """Check if we're running on EC2"""
    # Check if /var/www/yekar_coaches exists, which is our EC2 deployment path
    return os.path.exists('/var/www/yekar_coaches')

def run_command(cmd, cwd=None):
    """Run a command and handle potential errors"""
    try:
        subprocess.run(cmd, check=True, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        exit(1)

def main():
    # Determine if we're on EC2 or local
    on_ec2 = is_ec2()
    
    # Set base directory based on environment
    if on_ec2:
        base_dir = Path('/var/www/yekar_coaches')
    else:
        # Get the absolute path of the script's directory for local development
        base_dir = Path(__file__).parent.absolute()
    
    # Define paths relative to base directory
    frontend_dir = base_dir / 'frontend'
    frontend_build_dir = frontend_dir / 'build' / 'dist' / 'static' / 'frontend'
    backend_static_dir = base_dir / 'backend' / 'static' / 'frontend'

    print(f"Running in {'EC2' if on_ec2 else 'local'} environment")
    print(f"Base directory: {base_dir}")

    # Ensure directories exist
    frontend_build_dir.mkdir(parents=True, exist_ok=True)
    backend_static_dir.mkdir(parents=True, exist_ok=True)

    print("1. Cleaning frontend build directory...")
    if frontend_build_dir.exists():
        for item in frontend_build_dir.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    print("2. Building frontend...")
    run_command('npm run build', cwd=str(frontend_dir))

    print("3. Cleaning backend static directory...")
    if backend_static_dir.exists():
        for item in backend_static_dir.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    print("4. Moving built files to backend...")
    if not frontend_build_dir.exists():
        print("Error: Build directory does not exist after build")
        exit(1)

    # Move all files from frontend build to backend static
    if on_ec2:
        # On EC2, use cp command with preserve permissions
        run_command(f'cp -p {frontend_build_dir}/* {backend_static_dir}/')
    else:
        # On local, use Python's shutil
        for item in frontend_build_dir.glob('*'):
            dest_path = backend_static_dir / item.name
            if item.is_file():
                shutil.copy2(item, dest_path)
            elif item.is_dir():
                shutil.copytree(item, dest_path, dirs_exist_ok=True)

    print("Frontend update completed successfully!")

if __name__ == "__main__":
    main()
