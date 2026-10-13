from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                               QComboBox, QSpinBox, QHBoxLayout, QPushButton, 
                               QLabel, QDoubleSpinBox)
from PySide6.QtCore import Signal, Qt

class AddProductPanel(QWidget):

    product_submitted = Signal(dict)  # Signal to emit when a product is added

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(15)
        
        self.title_label = QLabel("Add New Product")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.main_layout.addWidget(self.title_label)
        
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(12)
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # Fields for Product Data Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., iPhone 15 Pro")
        
        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("Optional (Auto-generates if blank)")
        
        self.category_input = QComboBox()
        self.category_input.addItems(["Electronics", "Apparel", "Logistics", "Office Supplies"])
        
        self.qty_input = QSpinBox()
        self.qty_input.setRange(0, 99999)
        self.qty_input.setSuffix(" units")
        self.qty_input.setMinimumWidth(100)

        self.alert_threshold_input = QSpinBox()
        self.alert_threshold_input.setRange(0, 1000)
        self.alert_threshold_input.setValue(5)  # Default low-stock warning floor
        self.alert_threshold_input.setSuffix(" units")
        self.alert_threshold_input.setMinimumWidth(100)
        
        # Cost Data Input Field
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.00, 999999.00)
        self.price_input.setPrefix("$ ")
        self.price_input.setDecimals(2)
        
        # Main layout
        self.form_layout.addRow("Product Name *", self.name_input)
        self.form_layout.addRow("SKU / Barcode", self.sku_input)
        self.form_layout.addRow("Category", self.category_input)
        self.form_layout.addRow("Initial Stock", self.qty_input)
        self.form_layout.addRow("Alert Threshold", self.alert_threshold_input)
        self.form_layout.addRow("Unit Price ($)", self.price_input)
        
        self.main_layout.addLayout(self.form_layout)

        self.main_layout.addStretch()
        
        # Action Buttons
        self.save_btn = QPushButton("Save Product")
        self.save_btn.setFixedHeight(36)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4; 
                color: white; 
                font-weight: bold; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #106EBE; }
            QPushButton:pressed { background-color: #005A9E; }
        """)
        
        self.main_layout.addWidget(self.save_btn)
        
        # Connect visual interactions
        self.save_btn.clicked.connect(self.handle_save)

    def handle_save(self):
        """Validates inputs."""

        product_name = self.name_input.text().strip()
        if not product_name:
            self.name_input.setStyleSheet("border: 1px solid red;")
            self.name_input.setPlaceholderText("Name is required!")
            return
        
        # Reset border styles
        self.name_input.setStyleSheet("")
        
        form_data = {
            "name": product_name,
            "sku": self.sku_input.text().strip(),
            "category": self.category_input.currentText(),
            "quantity": self.qty_input.value(),
            "alert_threshold": self.alert_threshold_input.value(),
            "price": self.price_input.value()
        }
        
        self.product_submitted.emit(form_data)
        
        self.clear_form()
        
    def clear_form(self):
        """Resets the UI form"""
        self.name_input.clear()
        self.sku_input.clear()
        self.category_input.setCurrentIndex(0)
        self.qty_input.setValue(0)
        self.alert_threshold_input.setValue(5)
        self.price_input.setValue(0.00)
