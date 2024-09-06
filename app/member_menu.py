# app/member_menu.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QWidget
from app.member_registration import MemberRegistrationForm
from app.car import Car
from app.member import Member
class MemberMenu(QMainWindow):
    def __init__(self, system, main_window):
        super().__init__()
        self.system = system
        self.main_window = main_window  # Reference to the main window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Member Menu")
        self.setGeometry(100, 100, 600, 400)

        # List to display members
        self.member_list = QListWidget(self)
        self.populate_member_list()

        # Buttons for adding, editing, deleting, and going back to the main menu
        add_member_button = QPushButton("Add Member", self)
        add_member_button.clicked.connect(self.open_add_member)

        edit_member_button = QPushButton("Edit Member", self)
        edit_member_button.clicked.connect(self.edit_selected_member)

        delete_member_button = QPushButton("Delete Member", self)
        delete_member_button.clicked.connect(self.delete_selected_member)

        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.go_back_to_main_menu)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.member_list)
        layout.addWidget(add_member_button)
        layout.addWidget(edit_member_button)
        layout.addWidget(delete_member_button)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_member_list(self):
        """Populate the list of members in real-time"""
        self.member_list.clear()
        members = self.system.get_all_members()
        if not members:
            self.member_list.addItem("No members available")
        else:
            # Access Member attributes directly instead of treating them as a dictionary
            for member in members:
                car_info = ', '.join([car.plate_number for car in member.cars])  # Extract car plate numbers
                self.member_list.addItem(f"{member.name} - {member.house_number} - {car_info}")

    def open_add_member(self):
        """Open the Add Member form"""
        self.add_member_form = MemberRegistrationForm(self.system, self)
        self.add_member_form.show()

    # app/member_menu.py

    def edit_selected_member(self):
        """Edit the selected member"""
        selected_item = self.member_list.currentItem()
        if selected_item and selected_item.text() != "No members available":
            member_info = selected_item.text().split(" - ")
            member_name = member_info[0]
            member_data = self.system.get_member_by_name(member_name)

            if member_data:
                # Convert the MongoDB result back into a Member object
                cars = [Car(car['brand'], car['plate_number']) for car in member_data['cars']]
                member = Member(
                    name=member_data['name'],
                    house_number=member_data['house_number'],
                    cars=cars,
                    member_type=member_data['type']
                )

                # Populate the form with the member data
                self.edit_member_form = MemberRegistrationForm(self.system, self)
                self.edit_member_form.populate_form(member)
                self.edit_member_form.show()


    def delete_selected_member(self):
        """Delete the selected member"""
        selected_item = self.member_list.currentItem()
        if selected_item and selected_item.text() != "No members available":
            member_info = selected_item.text().split(" - ")
            member_name = member_info[0]
            reply = QMessageBox.question(self, "Delete Member", f"Are you sure you want to delete {member_name}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.system.delete_member_by_name(member_name)
                self.populate_member_list()  # Refresh the list after deletion

    def go_back_to_main_menu(self):
        """Return to the Main Menu"""
        self.main_window.show()
        self.close()
