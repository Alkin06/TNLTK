from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, \
    QHBoxLayout
from models.kanaryaBot.chatbot import generate_response


class ChatbotWorker(QThread):
    response_complete = Signal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        response = generate_response(self.question)
        self.response_complete.emit(response)


class ChatbotComponent(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.worker = None

    def initUI(self):
        layout = QVBoxLayout()

        # Initialize QListWidget for displaying messages
        self.message_list = QListWidget(self)
        layout.addWidget(self.message_list)

        input_layout = QHBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(50)
        input_layout.addWidget(self.text_edit)

        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def send_message(self):
        user_text = self.text_edit.toPlainText()
        if user_text:
            self.add_message("Siz:\n" + user_text, 'user')
            self.text_edit.clear()
            self.worker = ChatbotWorker(user_text)
            self.worker.response_complete.connect(self.add_bot_response)
            self.worker.start()

    def add_message(self, text, sender):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        if sender == 'user':
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.message_list.addItem(item)
        self.message_list.scrollToBottom()

    def add_bot_response(self, response):
        self.add_message("Bot:\n" + response, 'bot')
