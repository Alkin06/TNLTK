from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QDesktopServices


class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Welcome label
        welcome_label = QLabel("Welcome to TNLTK")
        welcome_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Info label
        info_label = QLabel("TNLTK is a toolkit for natural language processing.")
        info_label.setFont(QFont('Arial', 14))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # PyPI site button
        pypi_button = QPushButton("Visit our PyPI site")
        pypi_button.setFont(QFont('Arial', 14))
        pypi_button.clicked.connect(self.openPyPISite)

        # Paper PDF button
        paper_button = QPushButton("Read our paper")
        paper_button.setFont(QFont('Arial', 14))
        paper_button.clicked.connect(self.openPaperPDF)

        # Icon button
        icon_button = QPushButton()
        icon_button.setIcon(QIcon('../resources/tnltk_icon.png'))
        icon_button.setIconSize(QSize(128, 128))  # Adjust icon size as needed
        icon_button.setFlat(True)

        layout.addWidget(icon_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addWidget(pypi_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(paper_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def openPyPISite(self):
        QDesktopServices.openUrl(QUrl("https://pypi.org"))

    def openPaperPDF(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile("../resources/FinalReport.pdf"))


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec())
