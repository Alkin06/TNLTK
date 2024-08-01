from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel


class SummarizationComponent(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.summarize_button = QPushButton('Summarize Text', self)
        self.summarize_button.clicked.connect(self.summarize_text)
        layout.addWidget(self.summarize_button)

        self.result_label = QLabel('Summary: ', self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def summarize_text(self):
        input_text = self.text_edit.toPlainText()
        result = self.perform_summarization(input_text)
        self.result_label.setText(f'Summary: {result}')

    def perform_summarization(self, text):
        return text
