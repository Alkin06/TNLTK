from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar

from PySide6.QtCore import Qt, QThread, Signal, QTimer
import sys

sys.path.append('../../models/TurkicASR/turkic_languages_model')
from models.TurkicASR.turkic_languages_model.Model_speechToText import main


class SpeechToTextWorker(QThread):
    recognition_complete = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        recognized_text, time = main(self.file_path)
        self.recognition_complete.emit(recognized_text)


class SpeechToTextComponent(QWidget):
    def __init__(self):
        super().__init__()
        self.dot_count = 0
        self.timer = QTimer()
        self.worker = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_button = QPushButton("Select Audio File")
        self.select_button.clicked.connect(self.selectAudioFile)
        layout.addWidget(self.select_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel(
            "<h3>Model Info</h3>"
            "<ul>"
            "<li><b>Model:</b> TurkicASR</li>"
            "<li><b>Average Accuracy:</b> 95%</li>"
            "<li><b>Pipeline:</b>Pre-processing + Turkic Languages Model</li>"
            "<li><b>Supports:</b> MP3, WAV</li>"
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

    def selectAudioFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.worker = SpeechToTextWorker(file_path)
            self.worker.recognition_complete.connect(self.displayRecognizedText)
            self.worker.started.connect(self.startProcessingAnimation)
            self.worker.finished.connect(self.stopProcessingAnimation)
            self.worker.start()

    def displayRecognizedText(self, text):
        self.result_label.setText(text)
