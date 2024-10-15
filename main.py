import customtkinter as ctk
import keyboard
import time
import threading
import webbrowser

class AutoTyperApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Tython")
        self.root.geometry("450x700")
        self.root.resizable(False, False)  # Prevent resizing
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.input_delay = ctk.DoubleVar(value=1.0)
        self.char_delay = ctk.DoubleVar(value=0.05)
        self.typing_active = False

        self.create_ui()
        self.register_hotkey()

    def create_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(main_frame, text="Tython", font=("Roboto", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Text input
        text_frame = ctk.CTkFrame(main_frame, fg_color="#2a2d2e", corner_radius=10)
        text_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(text_frame, text="Enter Text:", font=("Roboto", 14, "bold"), text_color="white").pack(pady=(10, 5), padx=10)
        self.text_area = ctk.CTkTextbox(text_frame, width=400, height=150, font=("Roboto", 12))
        self.text_area.pack(pady=(0, 10), padx=10)

        # Input Delay
        input_delay_frame = ctk.CTkFrame(main_frame, fg_color="#2a2d2e", corner_radius=10)
        input_delay_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(input_delay_frame, text="Input Delay (seconds):", font=("Roboto", 14, "bold"), text_color="white").pack(pady=(10, 5), padx=10)
        self.input_delay_slider = ctk.CTkSlider(input_delay_frame, from_=1.0, to=5.0, number_of_steps=49, variable=self.input_delay)
        self.input_delay_slider.pack(pady=(0, 5), padx=10, fill="x")
        self.input_delay_label = ctk.CTkLabel(input_delay_frame, text=f"Current Input Delay: {self.input_delay.get():.1f}s", font=("Roboto", 12, "bold"), text_color="white")
        self.input_delay_label.pack(pady=(0, 10), padx=10)
        self.input_delay_slider.configure(command=lambda value: self.update_delay_label(value, self.input_delay_label, "Input"))

        # Character Delay
        char_delay_frame = ctk.CTkFrame(main_frame, fg_color="#2a2d2e", corner_radius=10)
        char_delay_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(char_delay_frame, text="Character Delay (seconds):", font=("Roboto", 14, "bold"), text_color="white").pack(pady=(10, 5), padx=10)
        self.char_delay_slider = ctk.CTkSlider(char_delay_frame, from_=0.01, to=0.5, number_of_steps=49, variable=self.char_delay)
        self.char_delay_slider.pack(pady=(0, 5), padx=10, fill="x")
        self.char_delay_label = ctk.CTkLabel(char_delay_frame, text=f"Current Character Delay: {self.char_delay.get():.2f}s", font=("Roboto", 12, "bold"), text_color="white")
        self.char_delay_label.pack(pady=(0, 10), padx=10)
        self.char_delay_slider.configure(command=lambda value: self.update_delay_label(value, self.char_delay_label, "Character"))

        # Status
        status_frame = ctk.CTkFrame(main_frame, fg_color="#2a2d2e", corner_radius=10)
        status_frame.pack(fill="x", pady=10)
        self.status_label = ctk.CTkLabel(status_frame, text="Status: Idle", font=("Roboto", 14, "bold"), text_color="white")
        self.status_label.pack(pady=10, padx=10)

        # Action buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        ctk.CTkButton(button_frame, text="Start Typing (F6)", command=self.start_typing, 
                      font=("Roboto", 14), fg_color="blue", hover_color="#45a049", 
                      corner_radius=20, border_width=2, border_color="white").pack(side="left", expand=True, padx=5)
        ctk.CTkButton(button_frame, text="Stop Typing (F7)", command=self.stop_typing, 
                      font=("Roboto", 14), fg_color="blue", hover_color="#d32f2f", 
                      corner_radius=20, border_width=2, border_color="white").pack(side="left", expand=True, padx=5)

        # Reset button
        reset_button = ctk.CTkButton(main_frame, text="Reset Delays", command=self.reset_delays, 
                                     font=("Roboto", 14), fg_color="blue", hover_color="#FF9800", 
                                     corner_radius=20, border_width=2, border_color="white")
        reset_button.pack(pady=10)

        # Creator info
        creator_frame = ctk.CTkFrame(self.root, fg_color="#1e1e1e", corner_radius=0)
        creator_frame.pack(side="bottom", fill="x")
        creator_label = ctk.CTkLabel(creator_frame, text="made by ", font=("Roboto", 12, "bold"), text_color="white")
        creator_label.pack(side="left", padx=(10, 0), pady=5)
        creator_link = ctk.CTkLabel(creator_frame, text="@PavanMeka", font=("Roboto", 12, "bold"), text_color="#1da1f2", cursor="hand2")
        creator_link.pack(side="left", pady=5)
        creator_link.bind("<Button-1>", lambda e: self.open_github())

    def update_delay_label(self, value, label, delay_type):
        if delay_type == "Input":
            label.configure(text=f"Current Input Delay: {float(value):.1f}s")
        else:
            label.configure(text=f"Current Character Delay: {float(value):.2f}s")

    def register_hotkey(self):
        keyboard.add_hotkey("f6", self.start_typing)
        keyboard.add_hotkey("f7", self.stop_typing)

    def start_typing(self):
        if not self.typing_active:
            self.typing_active = True
            self.status_label.configure(text="Status: Active", text_color="#4CAF50")
            threading.Thread(target=self.type_text, daemon=True).start()

    def stop_typing(self):
        self.typing_active = False
        self.status_label.configure(text="Status: Idle", text_color="white")

    def type_text(self):
        text = self.text_area.get("1.0", "end-1c")
        if not text.strip():
            return

        time.sleep(self.input_delay.get())

        for char in text:
            if not self.typing_active:
                break
            keyboard.write(char)
            time.sleep(self.char_delay.get())

        self.stop_typing()

    def reset_delays(self):
        self.input_delay.set(1.0)
        self.char_delay.set(0.05)
        self.update_delay_label(1.0, self.input_delay_label, "Input")
        self.update_delay_label(0.05, self.char_delay_label, "Character")
        self.input_delay_slider.set(1.0)
        self.char_delay_slider.set(0.05)

    def open_github(self):
        webbrowser.open("https://github.com/PavanMeka09")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoTyperApp()
    app.run()
