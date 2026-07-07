import os
import logging
import customtkinter as ctk
from gui.login import AdminLoginWindow
from gui.dashboard import SmartAttendDashboard

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def ensure_directories():
    base_dir = os.path.dirname(__file__)
    dirs = ["dataset", "models", "reports", "logs", "unknown_faces", "assets"]
    for d in dirs:
        path = os.path.join(base_dir, d)
        if not os.path.exists(path):
            os.makedirs(path)

class AppOrchestrator:
    def __init__(self):
        self.login_win = None
        self.dashboard_win = None
        self.show_login()

    def show_login(self):
        self.login_win = AdminLoginWindow(on_login_success=self.show_dashboard)
        self.login_win.mainloop()

    def show_dashboard(self):
        self.dashboard_win = SmartAttendDashboard(on_logout=self.show_login)
        self.dashboard_win.mainloop()

def main():
    try:
        ensure_directories()
        setup_logging()
        logging.info("Application session started.")
        
        # Enable CustomTkinter high-DPI scaling
        ctk.set_appearance_mode("dark")
        
        # Start orchestrator
        AppOrchestrator()
        
    except Exception as e:
        logging.critical(f"App boot failure: {str(e)}", exc_info=True)
        print(f"App failed to start. View logs/app.log for details.\nError: {e}")

if __name__ == "__main__":
    main()
