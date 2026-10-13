from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QTableView, QAbstractItemView, QHeaderView, QFrame, QApplication
from add_product_panel import AddProductPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.resize(1100, 700)
        self.setMinimumSize(900, 500)

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        self.setup_top_bar()
        self.setup_body_content()

        self.setStyleSheet("QSpinBox { padding-right: 24px; }"
        "QDoubleSpinBox { padding-right: 24px; }")

    def setup_top_bar(self):
        """Search bar, category filters, and action buttons."""
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(10)
        
        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by product name or ID...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedHeight(36)
        
        # Category Filter Dropdown
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")

        # Placeholder categories
        self.category_filter.addItems(["Electronics", "Apparel", "Logistics", "Office Supplies"])
        self.category_filter.setFixedHeight(36)
        self.category_filter.setFixedWidth(180)
        
        # Add Product
        self.add_product_btn = QPushButton("+ Add Product")
        self.add_product_btn.setCheckable(True) # Stays toggled down when clicked
        self.add_product_btn.setFixedHeight(36)
        self.add_product_btn.setFixedWidth(140)
        
        # Top Bar
        top_bar_layout.addWidget(self.search_input, stretch=1)
        top_bar_layout.addWidget(self.category_filter)
        top_bar_layout.addWidget(self.add_product_btn)
        
        self.main_layout.addLayout(top_bar_layout)

    def setup_body_content(self):
        """Creates the main body layout with the product table and side drawer for adding products."""
        self.body_layout = QHBoxLayout()
        self.body_layout.setSpacing(15)

        # Table View for Products
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False) 
        
        # Side Panel
        self.side_drawer = QFrame()
        self.side_drawer.setFrameShape(QFrame.StyledPanel)
        self.side_drawer.setFixedWidth(340) 
        self.side_drawer.setStyleSheet("background-color: #fcfcfc; border: 1px solid #dcdcdc; border-radius: 6px;")
        
        self.drawer_layout = QVBoxLayout(self.side_drawer)
        self.drawer_layout.setContentsMargins(12, 12, 12, 12)

        # Add Product Form
        self.add_product_form = AddProductPanel()
        self.drawer_layout.addWidget(self.add_product_form)
        
        self.side_drawer.hide()
        
        self.body_layout.addWidget(self.table_view, stretch=3)
        self.body_layout.addWidget(self.side_drawer, stretch=1)
        
        self.main_layout.addLayout(self.body_layout)
        
        self.add_product_btn.clicked.connect(self.toggle_side_drawer)

    def toggle_side_drawer(self, checked):
        """Shows or hides the side drawer."""
        if checked:
            self.side_drawer.show()
            self.add_product_btn.setText("Close Drawer")
        else:
            self.side_drawer.hide()
            self.add_product_btn.setText("+ Add Product")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()