import sys
import os
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListView, QLabel, QStyleFactory, QPushButton, QHBoxLayout
from PyQt5.QtCore import QStringListModel, Qt, QPoint
import pandas as pd

#i want the current dir from os
current_dir = os.path.dirname(os.path.realpath(__file__))
excellfile = os.path.join(current_dir, 'bk3data.xlsx')

# Load the Excel file
df = pd.read_excel(excellfile, engine='openpyxl')

# Generate a list of combined strings for unique values of both 'gatuadress' and 'begränsning'
combined_values = df.drop_duplicates(subset=['gatuadress', 'postnummer'])
unique_combined = [f"{row['gatuadress']} - {row['postnummer']}" for _, row in combined_values.iterrows()]
display_data = [f"{row['gatuadress']} - {row['postnummer']} | {row['begränsning']}" for _, row in combined_values.iterrows()]

class ListViewDemo(QWidget):
    def __init__(self, parent=None):
        super(ListViewDemo, self).__init__(parent)
        self.oldPos = self.pos()
        # QVBoxLayout and Widgets
        self.vbox = QVBoxLayout(self)
        self.le = QLineEdit()
        self.lv = QListView()
        self.label = QLabel()
        self.title = QLabel('Autocomplete Search')
        self.title.setStyleSheet("QLabel { font: bold; color: #EEE; }")
        self.button_exit = QPushButton('X')
        self.button_exit.clicked.connect(self.close)
        self.button_exit.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: #EEE;
                border: none;
                font: bold;
            }
            QPushButton:hover {
                background-color: #EEE;
                color: #333;
            }
        """)

        # Title bar layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.title)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.button_exit)
        self.vbox.addLayout(self.hbox)

        # Set QLineEdit and QListView to QVBoxLayout
        self.vbox.addWidget(self.le)
        self.vbox.addWidget(self.lv)
    
        # QStringListModel
        self.model = QStringListModel()
        self.model.setStringList(display_data)
        self.lv.setModel(self.model)

        # QLineEdit text changed connect to ListView update_model method
        self.le.textChanged.connect(self.update_model)

        # QWidget Settings
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Autocomplete Search')

        # Load window size from previous run
        try:
            with open('window_geometry.pickle', 'rb') as f:
                self.restoreGeometry(pickle.load(f))
        except (FileNotFoundError, EOFError):
            pass

        self.setStyleSheet("""
        QWidget {
        background-color: #333;
        }
        QLineEdit, QListView {
        color: #EEE;
        }
        QLineEdit {
        background-color: #555;
        }
        QListView {
        background-color: #555;
        show-decoration-selected: 1;
        }
        QListView::item {
        color: #EEE;
        background-color: #555;
        padding: 5px;
        border-bottom: 1px solid #EEE;  # This adds a border at the bottom
        }
        QListView::item:last-child {
        border-bottom: none;  # No border for the last item
        }
        QListView::item:selected {
        color: #333;
        background-color: #EEE;
        }
        """)


        self.lv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(max([self.fontMetrics().boundingRect(item).width() for item in unique_combined]))

        self.show()

    def update_model(self, text):
        search_terms = text.lower().split()
        matched_indices = [i for i, description in enumerate(unique_combined)
                        if all(term in description.lower() for term in search_terms)]
        
        matched_display_data = [display_data[i] for i in matched_indices]
        self.model.setStringList(matched_display_data)


    def closeEvent(self, event):
        # Save window size on closing
        with open('window_geometry.pickle', 'wb') as f:
            pickle.dump(self.saveGeometry(), f)

        super().closeEvent(event)
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    main = ListViewDemo()
    sys.exit(app.exec_())
