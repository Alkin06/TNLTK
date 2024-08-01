from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea, QFileDialog

from models.bertTurkishBased.bert_keyword import extract_keywords


class KeywordExtractionWorker(QThread):
    extraction_complete = Signal(str)

    def __init__(self, text=None, file_path=None):
        super().__init__()
        self.text = text
        self.file_path = file_path

    def run(self):
        result = None
        if self.text:
            print("self.text: " + self.text)
            result = extract_keywords(self.text)
        elif self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()
                print(self.text)
        result = extract_keywords(self.text)
        self.extraction_complete.emit(result)


class KeywordExtractionComponent(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.result_label = None
        self.summarize_button = None
        self.text_edit = None
        self.initUI()
        self.worker = None
        self.dot_count = 0
        self.timer = QTimer()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(200)
        layout.addWidget(self.text_edit)

        self.select_button = QPushButton('Select Text File', self)
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.summarize_button = QPushButton('Extract', self)
        self.summarize_button.clicked.connect(self.extractKeywords)
        layout.addWidget(self.summarize_button)

        self.result_area = QScrollArea(self)
        self.result_label = QLabel('Result: ', self)
        self.result_label.setWordWrap(True)
        self.result_area.setWidget(self.result_label)
        self.result_area.setWidgetResizable(True)
        self.result_area.setFixedHeight(200)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def startProcessingAnimation(self):
        self.dot_count = 0
        self.timer.timeout.connect(self.updateProcessingText)
        self.timer.start(500)  # Güncelleme aralığı (ms)

    def stopProcessingAnimation(self):
        self.timer.stop()

    def updateProcessingText(self):
        self.dot_count = (self.dot_count + 1) % 4  # 0, 1, 2, 3 döngüsü
        dots = '.' * self.dot_count
        self.result_label.setText(f"Processing{dots}")

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        if file_path:
            self.file_path = file_path

    def extractKeywords(self):
        input_text = self.text_edit.toPlainText()
        if input_text != "":
            self.worker = KeywordExtractionWorker(text=input_text)
        elif self.file_path:
            self.worker = KeywordExtractionWorker(file_path=self.file_path)
        else:
            self.result_label.setText('No text or file selecteddddddddddd')
            return

        self.worker.extraction_complete.connect(self.display_result)
        self.worker.started.connect(self.startProcessingAnimation)
        self.worker.finished.connect(self.stopProcessingAnimation)
        self.worker.start()

    def display_result(self, result):
        print("display_result: " + result)
        keywords = result.split(',')
        formatted_result = "Result:\n"
        for idx, keyword in enumerate(keywords, 1):
            formatted_result += f"{idx}. {keyword.strip()}\n"
        self.result_label.setText(formatted_result)
