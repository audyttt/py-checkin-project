# app/gui.py

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel, QMessageBox
from app.member_menu import MemberMenu
from app.staff_menu import StaffMenu
from app.system import System
from datetime import datetime
from app.guest_checkin_dialog import GuestCheckInDialog
from app.log_table import LogTable

class MainMenu(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Village Gate System")
        self.setGeometry(100, 100, 600, 300)

        # Create buttons
        member_button = QPushButton("Member Menu", self)
        member_button.clicked.connect(self.open_member_menu)

        log_table_button = QPushButton("Log Table", self)
        log_table_button.clicked.connect(self.open_log_table)  # Correct this line

        manage_staff_button = QPushButton("Manage Staff", self)
        manage_staff_button.clicked.connect(self.manage_staff)

        # Create a label and text input for license plate search
        plate_label = QLabel("Enter License Plate:")
        self.plate_input = QLineEdit(self)

        # Create a search button
        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.search_car)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(member_button)
        button_layout.addWidget(log_table_button)
        button_layout.addWidget(manage_staff_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(plate_label)
        main_layout.addWidget(self.plate_input)
        main_layout.addWidget(search_button)

        # Set the layout to a central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_member_menu(self):
        """Open the Member Menu"""
        self.member_menu_window = MemberMenu(self.system, self)
        self.member_menu_window.show()
        self.hide()

    def open_log_table(self):
        """Open the Log Table window."""
        self.log_table_window = LogTable(self.system)  # Create LogTable instance
        self.log_table_window.show()  # Show LogTable window

    def manage_staff(self):
        """Open the Staff Menu"""
        self.staff_menu_window = StaffMenu(self.system, self)
        self.staff_menu_window.show()
        self.hide()

    def search_car(self):
        """Search for a car by license plate and determine whether to show check-in or check-out for members or non-members."""
        plate_number = self.plate_input.text()

        # Clear any existing buttons before adding new ones
        self.clear_layout()

        # Check if the car belongs to a member
        car_data = self.system.get_member_by_plate(plate_number)

        if car_data:
            # Handle member case: check the last action for the member
            last_action = self.system.get_last_action(plate_number)
            if last_action == "check-in":
                self.confirm_checkout(plate_number, car_data['name'], car_data['house_number'])
            else:
                self.confirm_checkin(plate_number, car_data['name'], car_data['house_number'])
        else:
            # Handle non-member (guest) case
            last_action = self.system.get_last_log_for_guest(plate_number)

            if last_action and last_action["action"] == "Check-in":
                self.confirm_guest_checkout(last_action)
            else:
                self.register_car()

    def confirm_guest_checkout(self, last_log):
        """Confirm Check-out action for non-member and clear UI afterward"""
        plate_number = last_log["plate_number"]
        owner = last_log["owner"]
        house_number = last_log["house_number"]
        
        reply = QMessageBox.question(self, 'Confirm Guest Check-out', f"Do you want to check-out guest {plate_number} for {owner}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.check_out_car(plate_number, owner, house_number, "Guest")  # Log the check-out action for guest
        self.clear_layout()
        self.plate_input.clear()  # Clear the search input field

    def confirm_checkin(self, plate_number, owner, house_number):
        """Confirm Check-in action and clear UI afterward"""
        reply = QMessageBox.question(self, 'Confirm Check-in', f"Do you want to check-in {plate_number} for {owner}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.check_in_car(plate_number, owner, house_number, "Guest")
        self.clear_layout()
        self.plate_input.clear()  # Clear the search input field
        
    def confirm_checkout(self, plate_number, owner, house_number):
        """Confirm Check-out action for a member and clear UI afterward."""
        reply = QMessageBox.question(self, 'Confirm Check-out', f"Do you want to check-out {plate_number} for {owner}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.check_out_car(plate_number, owner, house_number, "Member")
        self.clear_layout()
        self.plate_input.clear()  # Clear the search input field


    def check_in_car(self, plate_number, owner, house_number, car_type):
        """Log the check-in action"""
        timestamp = datetime.now()
        active_staff = self.system.get_active_staff()
        self.system.log_action(plate_number, owner, house_number, "check-in", timestamp, car_type, active_staff)
        QMessageBox.information(self, "Check-in", f"{plate_number} checked in by {active_staff}.")

    def check_out_car(self, plate_number, owner, house_number, car_type):
        """Log the check-out action for the guest"""
        timestamp = datetime.now()
        active_staff = self.system.get_active_staff()
        self.system.log_action(plate_number, owner, house_number, "check-out", timestamp, car_type, active_staff)
        QMessageBox.information(self, "Check-out", f"{plate_number} (Guest) checked out by {active_staff}.")

    def register_car(self):
        """Open guest registration form for a non-member."""
        active_staff = self.system.get_active_staff()
        plate_number = self.plate_input.text()

        # Open the guest check-in dialog
        dialog = GuestCheckInDialog(plate_number, active_staff, self.system)
        dialog.exec_()  # Block the main window until the dialog is closed

        self.clear_layout()
        self.plate_input.clear()

    def clear_layout(self):
        """Clear dynamic buttons after check-in/check-out"""
        main_layout = self.centralWidget().layout()
        while main_layout.count() > 5:  # Keep the first few static elements
            item = main_layout.takeAt(5)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                    
    def open_log_table(self):
        """Open the Log Table window."""
        self.log_table_window = LogTable(self.system)
        self.log_table_window.show() 
