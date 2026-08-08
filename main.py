"""
main.py: This will be the main application.
"""

import sys

from PySide6.QtCore import Qt              # For window flags
from PySide6.QtGui import QPixmap          # For loading images/assets
from PySide6.QtWidgets import QApplication # For creating the application
import PySide6.QtWidgets as QtWidgets

from DesktopPet import DesktopPet



def main():

    # Create the application
    app = QApplication(sys.argv)

    pet = DesktopPet("Chi")
    pet.show()

    sys.exit(app.exec())









if __name__ == "__main__":
    main()