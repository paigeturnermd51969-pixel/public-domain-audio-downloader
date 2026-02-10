import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QTextEdit, QWidget, QCheckBox)
from PySide6.QtGui import (QCloseEvent, QTextCursor)
from PySide6.QtCore import (QObject, Signal)
from downloader import (download_album, download_song)

class StdOutWindow(QWidget):
    def __init__(self):
        super(StdOutWindow, self).__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('Loading Data')
        self.txt_edit = QTextEdit()
        layout.addWidget(self.txt_edit)
        self.setLayout(layout)
        self.setMinimumSize(600, 300)

        sys.stdout = EmittingStream()
        sys.stdout.text_written.connect(self.normal_output_written)

    def closeEvent(self, event: QCloseEvent) -> None:
        sys.stdout = sys.__stdout__
        event.accept()

    def normal_output_written(self, text):
        cursor = self.txt_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.txt_edit.setTextCursor(cursor)
        self.txt_edit.ensureCursorVisible()

class EmittingStream(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit()
        self.button = QPushButton("Download")
        self.checkbox = QCheckBox("Audio only")
        self.checkbox.setChecked(True)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
        # Window options
        self.setWindowTitle("Public Domain Audio Downloader")

    # Greets the user
    def greetings(self):
        print(f"Hello {self.edit.text()}")
        url = self.edit.text()
        if "&list=" in url:
            download_album(url, self.checkbox.isChecked())
        else:
            download_song(url, self.checkbox.isChecked())
        #download(self.edit.text())
    
    

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    #stdOutWindow = StdOutWindow()
    #stdOutWindow.show()
    # Run the main Qt loop
    sys.exit(app.exec())
