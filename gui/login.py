import customtkinter as ctk
from tkinter import messagebox
from database.db import DatabaseManager

class AdminLoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.db = DatabaseManager()

        # Window Configuration
        self.title("SmartAttend AI - Secure Admin Login")
        self.geometry("450x550")
        self.resizable(False, False)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (550 // 2)
        self.geometry(f"+{x}+{y}")

        # Set default theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    def setup_ui(self):
        # Background Container
        self.bg_frame = ctk.CTkFrame(self, width=400, height=500, corner_radius=15)
        self.bg_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.bg_frame, 
            text="SmartAttend AI", 
            font=ctk.CTkFont(family="Inter", size=26, weight="bold"),
            text_color="#3498db"
        )
        self.title_label.pack(pady=(40, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.bg_frame, 
            text="Secure Admin Portal", 
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#bdc3c7"
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Username Input
        self.username_label = ctk.CTkLabel(
            self.bg_frame, 
            text="Username", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold")
        )
        self.username_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.bg_frame, 
            placeholder_text="Enter admin username", 
            width=320, 
            height=40,
            corner_radius=8
        )
        self.username_entry.pack(padx=40, pady=(0, 15))
        self.username_entry.insert(0, "admin") # Set default for easy testing

        # Password Input
        self.password_label = ctk.CTkLabel(
            self.bg_frame, 
            text="Password", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold")
        )
        self.password_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.bg_frame, 
            placeholder_text="Enter password", 
            show="*", 
            width=320, 
            height=40,
            corner_radius=8
        )
        self.password_entry.pack(padx=40, pady=(0, 30))
        self.password_entry.insert(0, "admin123") # Set default for easy testing

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.bg_frame, 
            text="Login", 
            font=ctk.CTkFont(family="Inter", size=15, weight="bold"),
            width=320, 
            height=45,
            corner_radius=8,
            command=self.handle_login,
            hover_color="#2980b9"
        )
        self.login_btn.pack(padx=40, pady=10)

        # Footer Info
        self.footer_label = ctk.CTkLabel(
            self.bg_frame, 
            text="SmartAttend AI v2.0 • CS Final Year Project", 
            font=ctk.CTkFont(family="Inter", size=10),
            text_color="#7f8c8d"
        )
        self.footer_label.pack(side="bottom", pady=20)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all credentials.")
            return

        if self.db.validate_admin(username, password):
            self.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password.")

if __name__ == "__main__":
    def test_success():
        print("Success login mock called!")
    app = AdminLoginWindow(test_success)
    app.mainloop()
