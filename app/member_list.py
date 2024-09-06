# app/member_list.py

from PyQt5.QtWidgets import QMainWindow, QListWidget, QVBoxLayout, QWidget, QPushButton, QMessageBox
from app.member_registration import MemberRegistrationForm

class MemberList(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Member List")
        self.setGeometry(100, 100, 400, 300)

        # List to display members
        self.member_list = QListWidget(self)
        self.populate_member_list()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.member_list)

        # Buttons for adding, editing, and deleting members
        add_member_button = QPushButton("Add Member", self)
        add_member_button.clicked.connect(self.open_add_member)
        layout.addWidget(add_member_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_member_list(self):
        members = self.system.get_all_members()  # Retrieve members from the system
        if not members:
            self.member_list.addItem("No members available")
        else:
            for member in members:
                self.member_list.addItem(f"{member.name} - {member.house_number} - {member.license_plate}")

    def open_add_member(self):
        self.add_member_form = MemberRegistrationForm(self.system)
        self.add_member_form.show()
