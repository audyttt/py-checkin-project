# app/staff_registration.py

from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from app.staff import Staff

class StaffRegistrationForm(QMainWindow):
    def __init__(self, system, staff_menu):
        super().__init__()
        self.system = system
        self.staff_menu = staff_menu  # Reference to the staff menu for real-time refresh
        self.editing_staff = None  # Track if editing an existing staff member
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register Staff")
        self.setGeometry(100, 100, 400, 250)

        # Create the form labels and inputs
        name_label = QLabel("Name:")
        self.name_input = QLineEdit(self)

        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit(self)

        # Register Button
        register_button = QPushButton("Register", self)
        register_button.clicked.connect(self.register_staff)

        # Create the layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Add widgets to the layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(register_button)

        # Set the layout to the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_form(self, staff):
        """Populate the form with the selected staff member's data for editing."""
        self.editing_staff = staff  # Store the staff member being edited
        self.name_input.setText(staff.name)
        self.phone_input.setText(staff.phone_number)

    def register_staff(self):
        """Register or edit a staff member."""
        name = self.name_input.text()
        phone_number = self.phone_input.text()

        if self.editing_staff:
            # Edit existing staff
            updated_data = {"name": name, "phone_number": phone_number}
            self.system.update_staff(self.editing_staff.name, updated_data)
            QMessageBox.information(self, "Staff Updated", f"Staff {name}'s information was updated.")
        else:
            # Add a new staff member
            new_staff = Staff(name, phone_number)
            self.system.add_staff(new_staff)
            QMessageBox.information(self, "Staff Registered", f"New staff {name} was successfully registered.")

        # Refresh the staff list in the StaffMenu and close the form
        self.staff_menu.populate_staff_list()
        self.close()
