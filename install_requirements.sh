# Check for Python 3.6 installation
python_version=$(python3 --version)
required_version="Python 3.6"

if [ "$python_version" != "$required_version" ]; then
    echo "Installing Python 3.6"
    # Add commands to install Python 3.6 based on the operating system
    # For example, for Ubuntu:
    # sudo apt-get update
    # sudo apt-get install python3.6
else
    echo "Python 3.6 is already installed"
fi

# Install galois
pip install galois

# Install hashlib
pip install hashlib

# Install numpy
pip install numpy

#install math
pip install math

#install argparse
pip install argparse



