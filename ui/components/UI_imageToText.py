from PySide6.QtGui import QPixmap, QPainter, QPalette, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QSizePolicy, \
    QDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView

from PySide6.QtCore import Qt, QThread, Signal, QTimer
import sys

from models.DonutOCR.Model_imageToText import main


class ImageToTextWorker(QThread):
    recognition_complete = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        recognized_text = main(self.file_path)
        self.recognition_complete.emit(recognized_text)


class ImagePreviewDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Preview")
        self.setGeometry(100, 100, 800, 600)  # Genişlik ve yükseklik ayarlama

        layout = QVBoxLayout()
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        image = QImage(image_path)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

        self.setLayout(layout)


class ImageToTextComponent(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.initUI()
        self.timer = QTimer()
        self.dot_count = 0

    def initUI(self):
        layout = QVBoxLayout()

        self.select_button = QPushButton("Select Image File")
        self.select_button.clicked.connect(self.selectImageFile)
        layout.addWidget(self.select_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel(
            "<h3>Model Info</h3>"
            "<ul>"
            "<li><b>Model:</b> DonutOCR</li>"
            "<li><b>Average Accuracy:</b> 95%</li>"
            "<li><b>Pipeline:</b> DonutProcessor + VisionEncoderDecoderModel</li>"
            "<li><b>Supports:</b> PNG, JPG</li>"
            "</ul>"
        )
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
                    QLabel {
                        color: #2E4053;
                        background-color: #D6EAF8;
                        border: 1px solid #AED6F1;
                        border-radius: 5px;
                        padding: 10px;
                        font-family: Arial, sans-serif;
                    }
                    h3 {
                        margin: 0;
                        font-size: 18px;
                    }
                    ul {
                        padding-left: 20px;
                        margin: 0;
                    }
                    li {
                        margin-bottom: 5px;
                        font-size: 14px;
                    }
                """)
        layout.addWidget(self.info_label)

        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(200, 200)  # Sabit boyut
        self.image_label.setScaledContents(True)  # Resmi etiketin boyutuna ölçeklendir
        layout.addWidget(self.image_label)

        self.result_label = QLabel("Recognized Text will appear here")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        color: #1C2833;
                        padding: 10px;
                        border: 1px solid #B3B6B7;
                        border-radius: 5px;
                        background-color: #F2F4F4;
                    }
                """)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def startProcessingAnimation(self):
        self.dot_count = 0
        self.timer.timeout.connect(self.updateProcessingText)
        self.timer.start(500)  # Güncelleme aralığı (ms)

    def stopProcessingAnimation(self):
        self.timer.stop()
        # self.result_label.setText("Processing Complete")

    def updateProcessingText(self):
        self.dot_count = (self.dot_count + 1) % 4  # 0, 1, 2, 3 döngüsü
        dots = '.' * self.dot_count
        self.result_label.setText(f"Processing{dots}")

    def selectImageFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg)")
        if file_path:
            self.image_label.setPixmap(QPixmap(file_path))  # Resmi QLabel içine yerleştir
            self.image_label.setText("")  # Resim seçildiğinde metni temizle
            self.image_label.mousePressEvent = lambda event: self.showImagePreview(file_path)  # Tıklama olayı

            self.worker = ImageToTextWorker(file_path)
            self.worker.recognition_complete.connect(self.displayRecognizedText)
            self.worker.started.connect(self.startProcessingAnimation)
            self.worker.finished.connect(self.stopProcessingAnimation)
            self.worker.start()

    def showImagePreview(self, image_path):
        dialog = ImagePreviewDialog(image_path)
        dialog.exec()

    def displayRecognizedText(self, text):
        self.result_label.setText(text)
