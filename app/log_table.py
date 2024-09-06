# app/log_table.py

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class LogTable(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.current_page = 0  # Track the current page
        self.logs_per_page = 20  # Number of logs per page
        self.total_logs = self.system.get_log_count()  # Get the total number of logs
        self.total_pages = (self.total_logs + self.logs_per_page - 1) // self.logs_per_page  # Calculate total pages
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Log Table")
        self.setGeometry(100, 100, 800, 600)

        # Create the log table
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Plate Number", "Owner", "House Number", "Action", "Timestamp", "Staff"])

        # Create buttons for pagination
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        # Create a label to display the current page number
        self.page_label = QLabel(f"Page {self.current_page + 1} of {self.total_pages}", self)

        # Layout for pagination buttons and page label
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.next_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        # Set the layout to the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initially load the first page of logs
        self.load_logs()

    def load_logs(self):
        """Load logs for the current page."""
        self.table.setRowCount(0)  # Clear the table

        # Fetch logs for the current page
        logs = self.system.get_logs_by_page(self.current_page, self.logs_per_page)

        # Populate the table with logs
        for row_num, log in enumerate(logs):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(log['plate_number'])))  # Ensure str conversion
            self.table.setItem(row_num, 1, QTableWidgetItem(str(log['owner'])))
            self.table.setItem(row_num, 2, QTableWidgetItem(str(log['house_number'])))
            self.table.setItem(row_num, 3, QTableWidgetItem(str(log['action'])))
            self.table.setItem(row_num, 4, QTableWidgetItem(str(log['timestamp'])))  # Convert timestamp to string
            self.table.setItem(row_num, 5, QTableWidgetItem(str(log['staff'])))


        # Update page label
        self.page_label.setText(f"Page {self.current_page + 1} of {self.total_pages}")

    def prev_page(self):
        """Go to the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_logs()

    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_logs()
