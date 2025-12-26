import os
import platform

# Detect operating system and use appropriate script
if platform.system() == "Windows":
    os.system("batch_scripts/_go00.bat")
else:  # Linux, macOS, Unix
    os.system("./shell_scripts/_go00.sh")
