import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QTextEdit, QWidget, QCheckBox, QLabel, QHBoxLayout)
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
        self.url = QLineEdit()
        self.proxy_ip = QLineEdit()
        self.proxy_port = QLineEdit()
        self.button = QPushButton("Download")
        self.checkbox = QCheckBox("Audio only")
        self.checkbox.setChecked(True)
        # Create layout and add widgets
        layout = QVBoxLayout()

        url_row = QHBoxLayout()
        url_row.addWidget(QLabel("URL"))
        url_row.addWidget(self.url)
        layout.addLayout(url_row)

        proxy_ip_row = QHBoxLayout()
        proxy_ip_row.addWidget(QLabel("Proxy IP"))
        proxy_ip_row.addWidget(self.proxy_ip)
        layout.addLayout(proxy_ip_row)

        proxy_port_row = QHBoxLayout()
        proxy_port_row.addWidget(QLabel("Proxy Port"))
        proxy_port_row.addWidget(self.proxy_port)
        layout.addLayout(proxy_port_row)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
        # Window options
        self.setWindowTitle("Public Domain Audio Downloader")

    def greetings(self):
        url = self.url.text()

        proxy_ip = self.proxy_ip.text()
        proxy_port = self.proxy_port.text()
        proxy = ""
        if proxy_ip and proxy_port:
            proxy = proxy_ip + ":" + proxy_port

        if "&list=" in url:
            download_album(url, self.checkbox.isChecked(), proxy)
        else:
            download_song(url, self.checkbox.isChecked(), proxy)
    
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
