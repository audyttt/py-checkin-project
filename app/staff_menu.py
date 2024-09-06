# app/staff_menu.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QWidget
from app.staff_registration import StaffRegistrationForm
from app.staff import Staff

class StaffMenu(QMainWindow):
    def __init__(self, system, main_window):
        super().__init__()
        self.system = system
        self.main_window = main_window  # Reference to the main window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Staff Menu")
        self.setGeometry(100, 100, 600, 400)

        # List to display staff members
        self.staff_list = QListWidget(self)
        self.populate_staff_list()

        # Buttons for adding, editing, deleting, setting active, and going back to the main menu
        add_staff_button = QPushButton("Add Staff", self)
        add_staff_button.clicked.connect(self.open_add_staff)

        edit_staff_button = QPushButton("Edit Staff", self)
        edit_staff_button.clicked.connect(self.edit_selected_staff)

        delete_staff_button = QPushButton("Delete Staff", self)
        delete_staff_button.clicked.connect(self.delete_selected_staff)

        set_active_button = QPushButton("Set Active", self)  # New button for setting active staff
        set_active_button.clicked.connect(self.set_active_staff)

        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.go_back_to_main_menu)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.staff_list)
        layout.addWidget(add_staff_button)
        layout.addWidget(edit_staff_button)
        layout.addWidget(delete_staff_button)
        layout.addWidget(set_active_button)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_staff_list(self):
        """Populate the list of staff members in real-time"""
        self.staff_list.clear()
        staff_members = self.system.get_all_staff()
        if not staff_members:
            self.staff_list.addItem("No staff members available")
        else:
            for staff in staff_members:
                active_status = " (Active)" if staff.active else ""
                self.staff_list.addItem(f"{staff.name} - {staff.phone_number}{active_status}")

    def open_add_staff(self):
        """Open the Add Staff form"""
        self.add_staff_form = StaffRegistrationForm(self.system, self)
        self.add_staff_form.show()

    def edit_selected_staff(self):
        """Edit the selected staff member"""
        selected_item = self.staff_list.currentItem()
        if selected_item and selected_item.text() != "No staff members available":
            staff_info = selected_item.text().split(" - ")
            staff_name = staff_info[0]
            staff_data = self.system.get_staff_by_name(staff_name)

            if staff_data:
                staff = Staff(name=staff_data['name'], phone_number=staff_data['phone_number'])

                # Populate the form with the staff member data
                self.edit_staff_form = StaffRegistrationForm(self.system, self)
                self.edit_staff_form.populate_form(staff)
                self.edit_staff_form.show()

    def delete_selected_staff(self):
        """Delete the selected staff member"""
        selected_item = self.staff_list.currentItem()
        if selected_item and selected_item.text() != "No staff members available":
            staff_info = selected_item.text().split(" - ")
            staff_name = staff_info[0]
            reply = QMessageBox.question(self, "Delete Staff", f"Are you sure you want to delete {staff_name}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.system.delete_staff_by_name(staff_name)
                self.populate_staff_list()  # Refresh the list after deletion

    def set_active_staff(self):
        """Set the selected staff member as active"""
        selected_item = self.staff_list.currentItem()
        if selected_item and selected_item.text() != "No staff members available":
            staff_info = selected_item.text().split(" - ")
            staff_name = staff_info[0]
            self.system.set_active_staff(staff_name)
            QMessageBox.information(self, "Active Staff", f"{staff_name} is now the active staff member.")
            self.populate_staff_list()  # Refresh the list to show the active staff

    def go_back_to_main_menu(self):
        """Return to the Main Menu"""
        self.main_window.show()
        self.close()
