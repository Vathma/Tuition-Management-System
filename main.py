# main.py
import sys
import os

# Add the project root directory to sys.path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.login import LoginApp  

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
