# main.py

from PyQt5.QtWidgets import QApplication
from app.gui import MainMenu
from app.database import Database
from app.system import System

if __name__ == "__main__":
    # Initialize the database
    db = Database().get_db()
    system = System(db)

    # Start the main application window
    app = QApplication([])
    main_window = MainMenu(system)
    main_window.show()
    app.exec_()
