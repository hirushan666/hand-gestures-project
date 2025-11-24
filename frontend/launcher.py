import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence

# Import mode runner for threading-based execution
try:
    from mode_runners import ModeRunner
    USE_THREADING = True
    print("[Launcher] ModeRunner imported successfully")
except ImportError as e:
    USE_THREADING = False
    print(f"[Launcher] Warning: mode_runners not found ({e}), using subprocess mode")


class InstructionWindowNormal(tk.Toplevel):
    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.title("Normal Mouse Instructions")
        self.geometry("450x550")
        self.configure(bg="#1e1e2f")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self, text="📘 Normal Mouse Instructions", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=10)
        
        # GIF
        self.create_gif_label()
        
        # Instructions
        frame = tk.Frame(self, bg="#2c2c40", bd=2, relief=tk.RIDGE)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD, bg="#2c2c40", fg="#f2f2f2",
                      font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        text.insert("1.0", 
            "Welcome to Normal Mouse Mode!\n\n"
            "👉 This mode provides:\n"
            "• Standard mouse control\n"
            "• Traditional cursor movement\n"
            "• Conventional click operations\n\n"
            "🖱 Use STOP button to terminate the mode.\n"
            "⚙ Ensure your camera is working properly.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Start button
        btn = tk.Button(self, text="🧭 Start Normal Mode", 
                       command=self.start_normal_mode,
                       bg="#2d89ef", fg="white", font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn.pack(pady=10)
        
    def create_gif_label(self):
        # Detect if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            gif_path = os.path.join(bundle_dir, "assets", "test.gif")
        else:
            gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "test.gif"))
        
        if os.path.exists(gif_path):
            try:
                self.gif_image = Image.open(gif_path)
                self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((200, 150))) 
                                  for frame in ImageSequence.Iterator(self.gif_image)]
                
                self.gif_label = tk.Label(self, bg="#1e1e2f")
                self.gif_label.pack(pady=10)
                self.current_frame = 0
                self.animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
    
    def animate_gif(self):
        if hasattr(self, 'gif_frames') and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(100, self.animate_gif)
    
    def start_normal_mode(self):
        self.launcher.stop_process()
        self.launcher.launch_mode("normal_mode.py", "Normal Mode")
        self.destroy()


class InstructionWindowGesture(tk.Toplevel):
    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.title("Gesture Mouse Instructions")
        self.geometry("450x550")
        self.configure(bg="#1e1e2f")
        
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self, text="📘 Gesture Mouse Instructions", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=10)
        
        self.create_gif_label()
        
        frame = tk.Frame(self, bg="#2c2c40", bd=2, relief=tk.RIDGE)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD, bg="#2c2c40", fg="#f2f2f2",
                      font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        text.insert("1.0", 
            "Welcome to Gesture Mouse Mode!\n\n"
            "👉 Control your computer with hand gestures:\n"
            "• Index finger up: Move cursor\n"
            "• Index + Thumb: Click\n"
            "• Multiple gestures for different actions\n\n"
            "🖱 Use STOP button to terminate the mode.\n"
            "⚙ Ensure good lighting and clear hand visibility.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        btn = tk.Button(self, text="🖐 Start Gesture Mode", 
                       command=self.start_gesture_mode,
                       bg="#2d89ef", fg="white", font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn.pack(pady=10)
    
    def create_gif_label(self):
        # Detect if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            gif_path = os.path.join(bundle_dir, "assets", "test.gif")
        else:
            gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "test.gif"))
        
        if os.path.exists(gif_path):
            try:
                self.gif_image = Image.open(gif_path)
                self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((200, 150))) 
                                  for frame in ImageSequence.Iterator(self.gif_image)]
                
                self.gif_label = tk.Label(self, bg="#1e1e2f")
                self.gif_label.pack(pady=10)
                self.current_frame = 0
                self.animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
    
    def animate_gif(self):
        if hasattr(self, 'gif_frames') and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(100, self.animate_gif)
        
    def start_gesture_mode(self):
        self.launcher.stop_process()
        self.launcher.launch_mode("AI_virtual_Mouse.py", "Gesture Mode")
        self.destroy()


class InstructionWindowPresentation(tk.Toplevel):
    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.title("Presentation Instructions")
        self.geometry("450x550")
        self.configure(bg="#1e1e2f")
        
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self, text="📘 Presentation Mode Instructions", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=10)
        
        self.create_gif_label()
        
        frame = tk.Frame(self, bg="#2c2c40", bd=2, relief=tk.RIDGE)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD, bg="#2c2c40", fg="#f2f2f2",
                      font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        text.insert("1.0", 
            "Welcome to Presentation Mode!\n\n"
            "👉 Perfect for presentations:\n"
            "• Navigate slides with gestures\n"
            "• Point and highlight content\n"
            "• Smooth transitions\n\n"
            "🖱 Use STOP button to terminate the mode.\n"
            "⚙ Position yourself clearly in camera view.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        btn = tk.Button(self, text="🎥 Start Presentation Mode", 
                       command=self.start_presentation_mode,
                       bg="#2d89ef", fg="white", font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn.pack(pady=10)
    
    def create_gif_label(self):
        # Detect if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            gif_path = os.path.join(bundle_dir, "assets", "test.gif")
        else:
            gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "test.gif"))
        
        if os.path.exists(gif_path):
            try:
                self.gif_image = Image.open(gif_path)
                self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((200, 150))) 
                                  for frame in ImageSequence.Iterator(self.gif_image)]
                
                self.gif_label = tk.Label(self, bg="#1e1e2f")
                self.gif_label.pack(pady=10)
                self.current_frame = 0
                self.animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
    
    def animate_gif(self):
        if hasattr(self, 'gif_frames') and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(100, self.animate_gif)
        
    def start_presentation_mode(self):
        self.launcher.stop_process()
        self.launcher.launch_mode("PresentationMode.py", "Presentation Mode")
        self.destroy()


class InstructionWindowGaming(tk.Toplevel):
    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.title("Gaming Instructions")
        self.geometry("450x550")
        self.configure(bg="#1e1e2f")
        
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self, text="📘 Gaming Mode Instructions", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=10)
        
        self.create_gif_label()
        
        frame = tk.Frame(self, bg="#2c2c40", bd=2, relief=tk.RIDGE)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD, bg="#2c2c40", fg="#f2f2f2",
                      font=("Segoe UI", 10), bd=0, padx=10, pady=10)
        text.insert("1.0", 
            "Welcome to Gaming Mode!\n\n"
            "👉 Optimized for gaming:\n"
            "• High-speed sensitivity\n"
            "• Rapid response gestures\n"
            "• Enhanced precision\n\n"
            "🖱 Use STOP button to terminate the mode.\n"
            "⚙ Ensure stable lighting for best tracking.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        btn = tk.Button(self, text="🎮 Start Gaming Mode", 
                       command=self.start_gaming_mode,
                       bg="#2d89ef", fg="white", font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn.pack(pady=10)
    
    def create_gif_label(self):
        # Detect if running as PyInstaller bundle
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            gif_path = os.path.join(bundle_dir, "assets", "test.gif")
        else:
            gif_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "test.gif"))
        
        if os.path.exists(gif_path):
            try:
                self.gif_image = Image.open(gif_path)
                self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((200, 150))) 
                                  for frame in ImageSequence.Iterator(self.gif_image)]
                
                self.gif_label = tk.Label(self, bg="#1e1e2f")
                self.gif_label.pack(pady=10)
                self.current_frame = 0
                self.animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
    
    def animate_gif(self):
        if hasattr(self, 'gif_frames') and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(100, self.animate_gif)
        
    def start_gaming_mode(self):
        self.launcher.stop_process()
        self.launcher.launch_mode("gamingMode.py", "Gaming Mode")
        self.destroy()


class MouseLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gesture Mouse Launcher")
        self.geometry("420x500")
        self.configure(bg="#1e1e2f")
        self.resizable(False, False)
        
        self.process = None
        self.instruction_window = None
        
        # Use threading-based mode runner if available (for EXE)
        if USE_THREADING:
            self.mode_runner = ModeRunner()
        else:
            self.mode_runner = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self, text="🖱️ Gesture Mouse Controller", 
                        font=("Segoe UI", 16, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=20)
        
        # Separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)
        
        # Status label
        self.label = tk.Label(self, text="Choose a mode to start.", 
                             font=("Segoe UI", 11), 
                             bg="#1e1e2f", fg="#e0e0e0")
        self.label.pack(pady=10)
        
        # Button frame
        btn_frame = tk.Frame(self, bg="#1e1e2f")
        btn_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Buttons
        buttons = [
            ("🖐 Gesture Mode", self.run_gesture_mouse),
            ("🧭 Normal Mode", self.run_normal_mode),
            ("🖼 Presentation Mode", self.run_presentation_mode),
            ("🎮 Gaming Mode", self.run_gaming_mode),
            ("⏹ Stop Running Mode", self.stop_process),
            ("📘 View Instructions", self.show_instructions),
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                          bg="#2d89ef", fg="white", font=("Segoe UI", 11, "bold"),
                          relief=tk.FLAT, padx=20, pady=12, cursor="hand2",
                          activebackground="#1e65c2")
            btn.pack(pady=5, fill=tk.X)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1e65c2"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2d89ef"))
    
    def launch_mode(self, script_name, mode_name):
        # Use threading-based execution if available (for bundled EXE)
        if USE_THREADING and self.mode_runner:
            print(f"[Launcher] Launching {mode_name} via threading...")
            if script_name == "AI_virtual_Mouse.py":
                success = self.mode_runner.start(self.mode_runner.run_gesture_mode)
            elif script_name == "normal_mode.py":
                success = self.mode_runner.start(self.mode_runner.run_normal_mode)
            elif script_name == "PresentationMode.py":
                success = self.mode_runner.start(self.mode_runner.run_presentation_mode)
            elif script_name == "gamingMode.py":
                success = self.mode_runner.start(self.mode_runner.run_gaming_mode)
            else:
                print(f"[Launcher] Mode {mode_name} not implemented")
                self.label.config(text=f"⚠ {mode_name} not yet implemented!")
                return
            
            if success:
                print(f"[Launcher] {mode_name} started successfully")
                self.label.config(text=f"✅ {mode_name} is running!")
            else:
                print(f"[Launcher] Failed to start {mode_name}")
                self.label.config(text="⚙️ Another mode is already running!")
            return
        
        # Fallback to subprocess mode (for development)
        if self.process is None:
            # Detect if running as PyInstaller bundle
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                bundle_dir = sys._MEIPASS
                base_dir = bundle_dir
                python_exec = sys.executable
                
                # Script is bundled in the core directory
                script_path = os.path.join(bundle_dir, "core", script_name)
                
                if not os.path.exists(script_path):
                    self.label.config(text=f"❌ {script_name} not found in bundle!")
                    print(f"Expected at: {script_path}")
                    return
                
                # Set PYTHONPATH to include core directory for imports
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.join(bundle_dir, 'core')
                
            else:
                # Running from source
                base_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Try to find Python executable (check multiple common locations)
                python_paths = [
                    sys.executable,  # Current Python interpreter
                    os.path.join(base_dir, "venv", "Scripts", "python.exe"),
                    os.path.join(base_dir, "..", "venv", "Scripts", "python.exe"),
                    "python",  # System Python
                ]
                
                python_exec = None
                for path in python_paths:
                    if path == "python" or os.path.exists(path):
                        python_exec = path
                        break
                
                if python_exec is None:
                    self.label.config(text="❌ Python executable not found!")
                    return
                
                # Try to find the script in multiple locations
                script_paths = [
                    os.path.join(base_dir, script_name),
                    os.path.join(base_dir, "..", script_name),
                    os.path.join(base_dir, "core", script_name),
                    os.path.join(base_dir, "..", "core", script_name),
                ]
                
                script_path = None
                for path in script_paths:
                    if os.path.exists(path):
                        script_path = path
                        break
                
                if script_path is None:
                    self.label.config(text=f"❌ {script_name} not found!")
                    print(f"Searched in: {script_paths}")
                    return
                
                env = os.environ.copy()
            
            try:
                # Launch the script
                self.process = subprocess.Popen([python_exec, script_path], env=env)
                self.label.config(text=f"✅ {mode_name} is running!")
                print(f"Started: {python_exec} {script_path}")
            except Exception as e:
                self.label.config(text=f"❌ Error starting {mode_name}!")
                print(f"Error: {e}")
        else:
            self.label.config(text="⚙️ Another mode is already running!")
    
    def run_gesture_mouse(self):
        self.instruction_window = InstructionWindowGesture(self)
    
    def run_normal_mode(self):
        self.instruction_window = InstructionWindowNormal(self)
    
    def run_presentation_mode(self):
        self.instruction_window = InstructionWindowPresentation(self)
    
    def run_gaming_mode(self):
        self.instruction_window = InstructionWindowGaming(self)
    
    def stop_process(self):
        # Stop threading-based mode if using mode runner
        if USE_THREADING and self.mode_runner:
            self.mode_runner.stop()
            self.label.config(text="🛑 Process stopped.")
            return
        
        # Stop subprocess-based mode
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)  # Wait up to 5 seconds
            except subprocess.TimeoutExpired:
                self.process.kill()  # Force kill if it doesn't terminate
            except Exception as e:
                print(f"Error stopping process: {e}")
            finally:
                self.process = None
                self.label.config(text="🛑 Process stopped.")
        else:
            self.label.config(text="⚠ No process running.")
    
    def show_instructions(self):
        info = tk.Toplevel(self)
        info.title("Instructions")
        info.geometry("400x350")
        info.configure(bg="#1e1e2f")
        
        title = tk.Label(info, text="📘 Gesture Mouse Instructions", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#1e1e2f", fg="#f2f2f2")
        title.pack(pady=20)
        
        text = tk.Text(info, wrap=tk.WORD, bg="#2c2c40", fg="#f2f2f2",
                      font=("Segoe UI", 10), bd=0, padx=20, pady=20)
        text.insert("1.0", 
            "Welcome to Gesture Mouse Launcher!\n\n"
            "👉 Available Modes:\n\n"
            "1️⃣ Gesture Mode – Control with hand gestures\n"
            "2️⃣ Normal Mode – Standard mouse control\n"
            "3️⃣ Presentation Mode – Slide navigation\n"
            "4️⃣ Gaming Mode – High-speed sensitivity\n\n"
            "🖱 Click any mode button to see detailed instructions "
            "and start that mode.\n\n"
            "⚙ Make sure your camera is connected and working properly.")
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def on_closing(self):
        """Handle window close event"""
        self.stop_process()
        self.destroy()


if __name__ == "__main__":
    app = MouseLauncher()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()