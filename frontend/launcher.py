import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class InstructionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructions")
        self.setGeometry(650, 350, 450, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f2f2f2;
                font-family: 'Segoe UI';
            }
            QTextEdit {
                background-color: #2c2c40;
                border-radius: 8px;
                padding: 10px;
                color: #f2f2f2;
                font-size: 13px;
            }
        """)
        layout = QVBoxLayout()
        label = QLabel("📘 Gesture Mouse Instructions")
        label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setText(
            "Welcome to Gesture Mouse Launcher!\n\n"
            "👉 Modes available:\n"
            "1️⃣ Gesture Mode – Control your mouse with hand gestures.\n"
            "2️⃣ Normal Mode – Standard control setup.\n"
            "3️⃣ Presentation Mode – Ideal for slideshows and media control.\n"
            "4️⃣ Gaming Mode – Adjusts input sensitivity for gaming.\n\n"
            "🖱️ Use the Stop button to terminate any mode.\n\n"
            "⚙️ Ensure your camera and Python environment are correctly set up."
        )
        layout.addWidget(instructions)
        self.setLayout(layout)

class MouseLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Mouse Launcher")
        self.setGeometry(600, 300, 420, 450)
        self.setWindowIcon(QIcon("mouse_icon.png"))
        self.process = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🖱️ Gesture Mouse Controller")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        self.label = QLabel("Choose a mode to start.")
        self.label.setFont(QFont("Segoe UI", 11))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.btn_gesture = QPushButton("🖐 Gesture Mode")
        self.btn_normal = QPushButton("🧭 Normal Mode")
        self.btn_presentation = QPushButton("🖼 Presentation Mode")
        self.btn_gaming = QPushButton("🎮 Gaming Mode")
        self.btn_stop = QPushButton("⏹ Stop Running Mode")
        self.btn_instructions = QPushButton("📘 View Instructions")

        self.btn_gesture.clicked.connect(self.run_gesture_mouse)
        self.btn_normal.clicked.connect(self.run_normal_mode)
        self.btn_presentation.clicked.connect(self.run_presentation_mode)
        self.btn_gaming.clicked.connect(self.run_gaming_mode)
        self.btn_stop.clicked.connect(self.stop_process)
        self.btn_instructions.clicked.connect(self.show_instructions)

        layout.addWidget(self.btn_gesture)
        layout.addWidget(self.btn_normal)
        layout.addWidget(self.btn_presentation)
        layout.addWidget(self.btn_gaming)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_instructions)

        self.setLayout(layout)
        self.apply_styles()
        self.instruction_window = None

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f2f2f2;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2d89ef;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e65c2;
            }
            QPushButton:pressed {
                background-color: #164c91;
            }
        """)

    def launch_mode(self, script_name, mode_name):
        if self.process is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            python_exec = os.path.join(base_dir, "../venv/Scripts/python.exe")
            script_path = os.path.join(base_dir, f"../core/{script_name}")
            if not os.path.exists(python_exec):
                self.label.setText("❌ Python executable not found!")
                return
            if not os.path.exists(script_path):
                self.label.setText(f"❌ {script_name} not found!")
                return
            self.process = subprocess.Popen([python_exec, script_path])
            self.label.setText(f"✅ {mode_name} is running!")
        else:
            self.label.setText(f"⚙️ {mode_name} is already running or another mode is active!")

    def run_gesture_mouse(self):
        self.launch_mode("AI_virtual_Mouse.py", "Gesture Mode")

    def run_normal_mode(self):
        self.launch_mode("normal_mode.py", "Normal Mode")

    def run_presentation_mode(self):
        self.launch_mode("presentation_mode.py", "Presentation Mode")

    def run_gaming_mode(self):
        self.launch_mode("gaming_mode.py", "Gaming Mode")

    def stop_process(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.label.setText("🛑 Process stopped.")
        else:
            self.label.setText("⚠️ No process is currently running.")

    def show_instructions(self):
        if self.instruction_window is None:
            self.instruction_window = InstructionWindow()
        self.instruction_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseLauncher()
    window.show()
    sys.exit(app.exec_())
