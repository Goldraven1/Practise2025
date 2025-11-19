from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter
from PyQt6.QtCore import Qt, QDate
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, CalendarPicker, 
                            ComboBox, DoubleSpinBox, PrimaryPushButton, PushButton)

class TransactionDialog(MessageBoxBase):
    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("Добавить транзакцию", self)
        self.transaction = transaction
        
        # Form widgets
        self.datePicker = CalendarPicker(self)
        self.datePicker.setDate(QDate.currentDate())
        
        self.typeComboBox = ComboBox(self)
        self.typeComboBox.addItems(['Income', 'Expense'])
        
        self.categoryEdit = LineEdit(self)
        self.categoryEdit.setPlaceholderText("Категория (Еда, Зарплата...)")
        
        self.amountSpinBox = DoubleSpinBox(self)
        self.amountSpinBox.setRange(0.01, 10000000.00)
        self.amountSpinBox.setValue(100.00)
        
        self.descEdit = LineEdit(self)
        self.descEdit.setPlaceholderText("Описание")

        # Layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.datePicker)
        self.viewLayout.addWidget(self.typeComboBox)
        self.viewLayout.addWidget(self.categoryEdit)
        self.viewLayout.addWidget(self.amountSpinBox)
        self.viewLayout.addWidget(self.descEdit)

        # Pre-fill if editing
        if transaction:
            self.titleLabel.setText("Редактировать транзакцию")
            # transaction: (id, date, type, category, amount, desc)
            qdate = QDate.fromString(transaction[1], "yyyy-MM-dd")
            self.datePicker.setDate(qdate)
            self.typeComboBox.setCurrentText(transaction[2])
            self.categoryEdit.setText(transaction[3])
            self.amountSpinBox.setValue(transaction[4])
            self.descEdit.setText(transaction[5])

        # Validation for buttons
        self.widget.setMinimumWidth(350)
        
        # Connect signals to update state if needed
        self.yesButton.setText("Сохранить")
        self.cancelButton.setText("Отмена")

    def get_data(self):
        return {
            'date': self.datePicker.date.toString("yyyy-MM-dd"),
            'type_': self.typeComboBox.currentText(),
            'category': self.categoryEdit.text().strip(),
            'amount': self.amountSpinBox.value(),
            'description': self.descEdit.text().strip()
        }
