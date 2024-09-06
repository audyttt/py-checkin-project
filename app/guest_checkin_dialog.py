# app/guest_checkin_dialog.py

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime

class GuestCheckInDialog(QDialog):
    def __init__(self, plate_number, active_staff, system):
        super().__init__()
        self.system = system
        self.plate_number = plate_number
        self.active_staff = active_staff
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Guest Check-in")

        # Create the form fields
        plate_label = QLabel("Plate Number:")
        self.plate_input = QLineEdit(self)
        self.plate_input.setText(self.plate_number)
        self.plate_input.setReadOnly(True)

        owner_label = QLabel("Owner (Guest):")
        self.owner_input = QLineEdit(self)

        house_label = QLabel("House Number:")
        self.house_input = QLineEdit(self)

        action_label = QLabel("Action:")
        self.action_input = QLineEdit(self)
        self.action_input.setText("Check-in")
        self.action_input.setReadOnly(True)

        timestamp_label = QLabel("Timestamp:")
        self.timestamp_input = QDateTimeEdit(self)
        self.timestamp_input.setDateTime(QDateTime.currentDateTime())
        self.timestamp_input.setReadOnly(True)

        type_label = QLabel("Type:")
        self.type_input = QLineEdit(self)
        self.type_input.setText("Guest")
        self.type_input.setReadOnly(True)

        staff_label = QLabel("Staff:")
        self.staff_input = QLineEdit(self)
        self.staff_input.setText(self.active_staff["name"])
        self.staff_input.setReadOnly(True)

        # Submit button
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.submit)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(plate_label)
        layout.addWidget(self.plate_input)
        layout.addWidget(owner_label)
        layout.addWidget(self.owner_input)
        layout.addWidget(house_label)
        layout.addWidget(self.house_input)
        layout.addWidget(action_label)
        layout.addWidget(self.action_input)
        layout.addWidget(timestamp_label)
        layout.addWidget(self.timestamp_input)
        layout.addWidget(type_label)
        layout.addWidget(self.type_input)
        layout.addWidget(staff_label)
        layout.addWidget(self.staff_input)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit(self):
        """Submit the guest check-in information and log the action."""
        plate_number = self.plate_input.text()
        owner = self.owner_input.text()
        house_number = self.house_input.text()
        action = self.action_input.text()
        timestamp = self.timestamp_input.dateTime().toPyDateTime()
        car_type = self.type_input.text()
        staff = self.staff_input.text()

        if not owner or not house_number:
            QMessageBox.warning(self, "Input Error", "Please fill in all the required fields.")
            return

        # Log the guest check-in action
        self.system.log_action(plate_number, owner, house_number, action, timestamp, car_type, staff)

        QMessageBox.information(self, "Check-in Complete", f"Guest {plate_number} checked in by {staff}.")
        self.accept()  # Close the dialog
