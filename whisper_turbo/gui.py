import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
import mlx_whisper

####################
# Code by Debugverse
# https://www.youtube.com/@DebugVerseTutorials
####################

class TranscriptionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("MP3 Transcriber")
        self.setGeometry(100, 100, 600, 400)

        # Layout and widgets
        self.layout = QVBoxLayout()

        self.label = QLabel("Upload an MP3 file for transcription")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Select MP3 File")
        self.button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.layout.addWidget(self.result_box)

        self.setLayout(self.layout)

    def open_file_dialog(self):
        # Open file dialog to select an MP3 file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open MP3 File", "", "MP3 Files (*.mp3)")

        if file_path:
            # Perform transcription
            try:
                transcription = mlx_whisper.transcribe(file_path, path_or_hf_repo="mlx-community/whisper-turbo")["text"]
                self.result_box.setText(transcription)
            except Exception as e:
                self.result_box.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the app window
    window = TranscriptionApp()
    window.show()

    # Execute the application
    sys.exit(app.exec_())
