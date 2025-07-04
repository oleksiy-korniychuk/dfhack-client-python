#!/usr/bin/env python3
"""
Script to generate Python protobuf code using cmake and make.
This script runs the cmake and make commands inside the /cmake directory.
It requires a DFHack git tag (e.g. 51.13-r1) to be passed as an argument.
"""

import argparse
import subprocess
import sys
import platform
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required tools are installed and accessible."""
    required_tools = ["cmake", "make", "protoc"]
    missing_tools = []
    
    for tool in required_tools:
        if shutil.which(tool) is None:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"Error: Missing required tools: {', '.join(missing_tools)}")
        print("Please install the missing tools and ensure they are in your PATH.")
        return False
    
    return True

def generate_windows(tag, cmake_dir):
    """Generate protobuf code on Windows using MinGW Makefiles."""
    subprocess.run([
        "cmake", "-G", "MinGW Makefiles", f"-DTAG={tag}", "."
    ], cwd=cmake_dir, check=True)
    
    subprocess.run(["make"], cwd=cmake_dir, check=True)

def generate_linux(tag, cmake_dir):
    """Generate protobuf code on Linux using Unix Makefiles."""
    subprocess.run([
        "cmake", "-G", "Unix Makefiles", f"-DTAG={tag}", "."
    ], cwd=cmake_dir, check=True)
    
    subprocess.run(["make"], cwd=cmake_dir, check=True)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate Python protobuf code"
    )
    parser.add_argument(
        "--tag",
        required=True,
        help="The DFHack git tag to use. the .proto files must already be in the ./proto/<tag> directory. (e.g., '51.13-r1')."
    )
    tag = parser.parse_args().tag
    
    if not check_dependencies():
        sys.exit(1)
    
    project_root = Path(__file__).parent.parent
    cmake_dir = project_root / "cmake"
    
    if platform.system() == "Windows":
        generate_windows(tag, cmake_dir)
    else:
        generate_linux(tag, cmake_dir)

if __name__ == "__main__":
    main()
