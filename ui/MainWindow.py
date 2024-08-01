import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QApplication, QPushButton, \
    QVBoxLayout
from ui.components.UI_TNLTK import WelcomeScreen
from ui.components.UI_sentimentAnalysis import SentimentAnalysisComponent
from ui.components.UI_speechToText import SpeechToTextComponent
from ui.components.UI_summarization import SummarizationComponent
from ui.components.UI_imageToText import ImageToTextComponent
from ui.components.UI_keywordExtraction import KeywordExtractionComponent
from components.UI_chatbot import ChatbotComponent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.components = [("Sentiment Analysis", SentimentAnalysisComponent()),
                           ("Summarization", SummarizationComponent()),
                           ("Keyword Extraction", KeywordExtractionComponent()),
                           ("Chatbot", ChatbotComponent()),
                           ("Speech To Text", SpeechToTextComponent()),
                           ("Image To Text", ImageToTextComponent())]
        self.welcome_screen = WelcomeScreen()
        self.stack = QStackedWidget(self)
        self.menu_list = QListWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TNLTK')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # Add TNLTK icon button
        icon_button = QPushButton()
        icon_button.setIcon(QIcon('resources/tnltk_icon.png'))
        icon_button.clicked.connect(self.showWelcomeScreen)
        icon_button.resize(150, 75)
        left_layout.addWidget(icon_button)

        self.addModelsToMenuList()
        self.menu_list.currentItemChanged.connect(self.displayComponent)
        left_layout.addWidget(self.menu_list)

        self.welcome_screen = WelcomeScreen()
        self.showWelcomeScreen()
        self.stack.addWidget(self.welcome_screen)
        main_layout.addWidget(self.stack)

        self.displayComponent()

    def addModelsToMenuList(self):
        for model in self.components:
            self.addNewModel(model[0], model[1])

    def addNewModel(self, modelName, modelPage):
        self.menu_list.addItem(modelName)
        self.stack.addWidget(modelPage)

    def displayComponent(self):
        current = self.menu_list.currentItem()
        if current:
            index = self.menu_list.row(current)
            self.stack.setCurrentIndex(index)
        else:
            self.stack.setCurrentWidget(self.welcome_screen)

    def showWelcomeScreen(self):
        self.stack.setCurrentWidget(self.welcome_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
