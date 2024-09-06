# app/member_registration.py

from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from app.member import Member
from app.car import Car

class MemberRegistrationForm(QMainWindow):
    def __init__(self, system, member_menu):
        super().__init__()
        self.system = system
        self.member_menu = member_menu  # Reference to the member menu for real-time refresh
        self.editing_member = None  # Track if editing an existing member
        self.car_inputs = []  # List to track car input fields (brand_input, plate_input, car_layout)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register Member")
        self.setGeometry(100, 100, 400, 350)

        # Create the form labels and inputs
        name_label = QLabel("Name:")
        self.name_input = QLineEdit(self)

        house_label = QLabel("House Number:")
        self.house_input = QLineEdit(self)

        # Create the layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Add main form fields
        self.layout.addWidget(name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(house_label)
        self.layout.addWidget(self.house_input)

        # Section for cars (dynamically generated car fields)
        self.cars_layout = QVBoxLayout()
        self.layout.addLayout(self.cars_layout)

        # Button to add a new car
        add_car_button = QPushButton("Add Car", self)
        add_car_button.clicked.connect(self.add_car_fields)
        self.layout.addWidget(add_car_button)

        # Register Button
        register_button = QPushButton("Register", self)
        register_button.clicked.connect(self.register_member)
        self.layout.addWidget(register_button)

        # Set the layout to the central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_car_fields(self, car=None):
        """Dynamically add car brand and plate fields."""
        car_layout = QHBoxLayout()

        # Car Brand input
        brand_input = QLineEdit(self)
        brand_label = QLabel("Car Brand:", self)
        if car:
            brand_input.setText(car.brand)

        # License Plate input
        plate_input = QLineEdit(self)
        plate_label = QLabel("License Plate:", self)
        if car:
            plate_input.setText(car.plate_number)

        # Add delete car button
        delete_car_button = QPushButton("Remove", self)
        delete_car_button.clicked.connect(lambda: self.remove_car_fields(car_layout, brand_input, plate_input))

        # Add inputs to the layout
        car_layout.addWidget(brand_label)
        car_layout.addWidget(brand_input)
        car_layout.addWidget(plate_label)
        car_layout.addWidget(plate_input)
        car_layout.addWidget(delete_car_button)

        # Track car input fields
        self.car_inputs.append((brand_input, plate_input, car_layout))
        self.cars_layout.addLayout(car_layout)

    def remove_car_fields(self, car_layout, brand_input, plate_input):
        """Remove a car's input fields from the form."""
        # Remove car input from tracking list
        self.car_inputs = [(b, p, l) for b, p, l in self.car_inputs if l != car_layout]

        # Remove the car layout from the UI
        for i in reversed(range(car_layout.count())):
            widget = car_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def populate_form(self, member):
        """Populate the form with the selected member's data for editing."""
        self.editing_member = member  # Store the member being edited
        self.name_input.setText(member.name)
        self.house_input.setText(member.house_number)

        # Clear previous car input fields
        while self.cars_layout.count():
            item = self.cars_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Populate form with the existing cars
        for car in member.cars:
            self.add_car_fields(car)

    def register_member(self):
        """Register or edit a member, including updating their car list."""
        name = self.name_input.text()
        house_number = self.house_input.text()

        cars = []
        for brand_input, plate_input, _ in self.car_inputs:
            car_brand = brand_input.text()
            plate_number = plate_input.text()
            if car_brand and plate_number:
                cars.append(Car(car_brand, plate_number))

        if self.editing_member:
            # Edit existing member's cars
            self.system.update_member_cars(self.editing_member.name, [{"brand": car.brand, "plate_number": car.plate_number} for car in cars])
            QMessageBox.information(self, "Member Updated", f"Member {name}'s information was updated.")

        else:
            # Add a new member
            new_member = Member(name, house_number, cars)
            self.system.add_member(new_member)
            QMessageBox.information(self, "Member Registered", f"New member {name} was successfully registered.")

        # Refresh the member list in the MemberMenu and close the form
        self.member_menu.populate_member_list()
        self.close()
