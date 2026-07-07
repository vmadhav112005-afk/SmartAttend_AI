import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import os
import cv2
import pandas as pd
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.db import DatabaseManager
from ai.training import FaceTrainer
from ai.recognition import FaceRecognizer

class SmartAttendDashboard(ctk.CTk):
    def __init__(self, on_logout):
        super().__init__()
        self.on_logout = on_logout
        self.db = DatabaseManager()

        # Window Configuration
        self.title("SmartAttend AI - Enterprise Dashboard")
        self.geometry("1100x700")
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (1100 // 2)
        y = (screen_height // 2) - (700 // 2)
        self.geometry(f"+{x}+{y}")

        # Config state
        self.appearance_mode = "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("blue")

        # Layout Setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()
        self.show_dashboard_home()

    # --- Side Navigation ---
    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Header Info
        self.app_title = ctk.CTkLabel(
            self.sidebar_frame, 
            text="SmartAttend AI", 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#3498db"
        )
        self.app_title.grid(row=0, column=0, padx=20, pady=(20, 2))

        self.app_version = ctk.CTkLabel(
            self.sidebar_frame, 
            text="v2.0 Enterprise", 
            font=ctk.CTkFont(family="Inter", size=11),
            text_color="#7f8c8d"
        )
        self.app_version.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Menu Buttons
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard_home),
            ("👤 Register Student", self.show_register_student),
            ("🧠 Train AI Model", self.show_train_model),
            ("📷 Live Attendance", self.start_live_attendance),
            ("📊 Analytics", self.show_analytics),
            ("📄 Reports", self.show_reports),
            ("⚙ Settings", self.show_settings),
        ]

        self.nav_buttons = {}
        for idx, (label, command) in enumerate(menu_items):
            btn = ctk.CTkButton(
                self.sidebar_frame, 
                text=label, 
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                font=ctk.CTkFont(family="Inter", size=13),
                command=command
            )
            btn.grid(row=idx+2, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[label] = btn

        # Theme Toggle
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame, 
            text="Light Mode", 
            command=self.toggle_theme
        )
        self.theme_switch.grid(row=11, column=0, padx=20, pady=15, sticky="s")

        # Logout Button
        self.logout_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="🚪 Logout", 
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self.handle_logout
        )
        self.logout_btn.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="s")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            self.appearance_mode = "light"
            self.theme_switch.configure(text="Dark Mode")
        else:
            self.appearance_mode = "dark"
            self.theme_switch.configure(text="Light Mode")
        ctk.set_appearance_mode(self.appearance_mode)

    def handle_logout(self):
        self.destroy()
        self.on_logout()

    # --- Main Frame Management ---
    def setup_main_frame(self):
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

    def clear_main_frame(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def set_nav_active(self, active_label):
        for label, btn in self.nav_buttons.items():
            if active_label in label:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

    # --- 🏠 Dashboard Home Screen ---
    def show_dashboard_home(self):
        self.clear_main_frame()
        self.set_nav_active("Dashboard")

        home_container = ctk.CTkScrollableFrame(self.main_content_frame, fg_color="transparent")
        home_container.pack(fill="both", expand=True)

        # Welcome Label
        welcome_lbl = ctk.CTkLabel(
            home_container, 
            text="Welcome back, Administrator", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold")
        )
        welcome_lbl.pack(anchor="w", pady=(10, 20))

        # Metrics Grid Frame
        metrics_frame = ctk.CTkFrame(home_container, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=10)
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Query metrics from DB
        total_students = self.db.get_student_count()
        today_attendance = self.db.get_today_attendance_count()
        
        # Calculate percentage
        attendance_percentage = 0.0
        if total_students > 0:
            attendance_percentage = (today_attendance / total_students) * 100

        # Count unknown faces
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        unknown_dir = os.path.join(base_dir, "unknown_faces")
        unknown_count = 0
        if os.path.exists(unknown_dir):
            unknown_count = len([f for f in os.listdir(unknown_dir) if f.endswith(('.jpg', '.png'))])

        cards = [
            ("👥 Total Students", str(total_students), "#3498db"),
            ("✅ Today's Attendance", str(today_attendance), "#2ecc71"),
            ("📈 Attendance Rate", f"{attendance_percentage:.1f}%", "#e67e22"),
            ("⚠️ Unknown Faces", str(unknown_count), "#e74c3c")
        ]

        for i, (title, val, color) in enumerate(cards):
            card = ctk.CTkFrame(metrics_frame, height=120, corner_radius=10)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            card.grid_propagate(False)
            
            lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Inter", size=13), text_color="#bdc3c7")
            lbl_title.pack(anchor="w", padx=15, pady=(15, 5))
            
            lbl_val = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(family="Inter", size=28, weight="bold"), text_color=color)
            lbl_val.pack(anchor="w", padx=15, pady=(0, 10))

        # Recent Activity Table Frame
        activity_frame = ctk.CTkFrame(home_container)
        activity_frame.pack(fill="both", expand=True, pady=20)
        
        act_title = ctk.CTkLabel(
            activity_frame, 
            text="Recent Activity Log (Today)", 
            font=ctk.CTkFont(family="Inter", size=16, weight="bold")
        )
        act_title.pack(anchor="w", padx=20, pady=15)

        # Matplotlib quick chart rendering directly in the homepage
        chart_container = ctk.CTkFrame(activity_frame, height=250, fg_color="transparent")
        chart_container.pack(fill="x", padx=20, pady=10)
        self.render_quick_chart(chart_container)

    def render_quick_chart(self, parent):
        fig = Figure(figsize=(8, 2.2), dpi=100)
        ax = fig.add_subplot(111)
        
        # Pull last 5 days attendance counts
        records = self.db.get_attendance_records()
        df = pd.DataFrame(records, columns=["student_id", "name", "date", "time", "status", "confidence"])
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            daily_counts = df.groupby('date').size().tail(5)
            dates = [d.strftime('%m-%d') for d in daily_counts.index]
            counts = daily_counts.values
        else:
            dates = ["No Data"]
            counts = [0]

        ax.bar(dates, counts, color="#3498db", width=0.4)
        ax.set_title("Recent Attendance Count", fontsize=9, color="#95a5a6")
        ax.tick_params(colors="#95a5a6", labelsize=8)
        
        # Color match matching theme
        bg_color = "#2b2b2b" if self.appearance_mode == "dark" else "#dbdbdb"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- 👤 Student Registration ---
    def show_register_student(self):
        self.clear_main_frame()
        self.set_nav_active("Register Student")

        reg_container = ctk.CTkFrame(self.main_content_frame)
        reg_container.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(
            reg_container, 
            text="Student Biometric Enrolment", 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#3498db"
        )
        title.pack(anchor="w", padx=30, pady=(30, 20))

        # Input Grid Frame
        grid = ctk.CTkFrame(reg_container, fg_color="transparent")
        grid.pack(anchor="w", padx=30, pady=10)

        fields = [
            ("Student ID", "id_entry", "e.g., CS-101"),
            ("Full Name", "name_entry", "e.g., Vansh"),
            ("Department", "dept_entry", "e.g., Computer Science"),
            ("Year", "year_entry", "e.g., 4th Year")
        ]

        self.reg_entries = {}
        for idx, (label, name, hint) in enumerate(fields):
            lbl = ctk.CTkLabel(grid, text=label, font=ctk.CTkFont(family="Inter", size=12, weight="bold"))
            lbl.grid(row=idx, column=0, padx=(0, 20), pady=10, sticky="w")
            
            entry = ctk.CTkEntry(grid, placeholder_text=hint, width=280)
            entry.grid(row=idx, column=1, pady=10, sticky="w")
            self.reg_entries[name] = entry

        # Capture Button
        btn_capture = ctk.CTkButton(
            reg_container, 
            text="Start Photo Capture (30 Samples)",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            fg_color="#27ae60",
            hover_color="#219a52",
            height=40,
            command=self.capture_biometric_samples
        )
        btn_capture.pack(anchor="w", padx=30, pady=30)

    def capture_biometric_samples(self):
        # Validate inputs
        student_id = self.reg_entries["id_entry"].get().strip()
        name = self.reg_entries["name_entry"].get().strip()
        dept = self.reg_entries["dept_entry"].get().strip()
        year = self.reg_entries["year_entry"].get().strip()

        if not all([student_id, name, dept, year]):
            messagebox.showerror("Error", "All registration fields are required.")
            return

        # Prepare dataset directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(base_dir, "dataset", f"{student_id}_{name}")
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        cam = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        count = 0
        messagebox.showinfo("Instructions", "Webcam will launch. Look straight into the camera.\nCapturing 30 samples. Press 'q' to abort.")

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                face_crop = frame[y:y+h, x:x+w]
                img_path = os.path.join(dataset_path, f"sample_{count}.jpg")
                cv2.imwrite(img_path, face_crop)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (46, 204, 113), 2)
                cv2.putText(frame, f"Captured: {count}/30", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Registering - Keep Looking at Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
                break

        cam.release()
        cv2.destroyAllWindows()

        if count >= 30:
            success, msg = self.db.add_student(student_id, name, dept, year, None)
            if success:
                messagebox.showinfo("Success", f"30 biometric samples registered for {name}.\nProceed to 'Train AI Model'.")
                # Clear fields
                for entry in self.reg_entries.values():
                    entry.delete(0, "end")
            else:
                messagebox.showerror("Database Error", msg)
        else:
            messagebox.showwarning("Cancelled", "Biometric enrollment was aborted.")

    # --- 🧠 Train AI Model ---
    def show_train_model(self):
        self.clear_main_frame()
        self.set_nav_active("Train AI Model")

        train_container = ctk.CTkFrame(self.main_content_frame)
        train_container.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(
            train_container, 
            text="AI Face Embeddings Pipeline", 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#e67e22"
        )
        title.pack(anchor="w", padx=30, pady=(30, 20))

        desc = ctk.CTkLabel(
            train_container, 
            text="This step generates 128-dimensional biometric embeddings from registered samples and updates the AI local weight configuration.",
            font=ctk.CTkFont(family="Inter", size=13),
            wraplength=600,
            justify="left"
        )
        desc.pack(anchor="w", padx=30, pady=10)

        # Progress bar
        self.train_progress = ctk.CTkProgressBar(train_container, width=500)
        self.train_progress.pack(anchor="w", padx=30, pady=30)
        self.train_progress.set(0)

        self.status_lbl = ctk.CTkLabel(
            train_container, 
            text="System Idle", 
            font=ctk.CTkFont(family="Inter", size=12, slant="italic")
        )
        self.status_lbl.pack(anchor="w", padx=30, pady=5)

        # Train button
        btn_train = ctk.CTkButton(
            train_container, 
            text="Run AI Pipeline",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            fg_color="#e67e22",
            hover_color="#d35400",
            height=40,
            command=self.run_ai_pipeline
        )
        btn_train.pack(anchor="w", padx=30, pady=20)

    def run_ai_pipeline(self):
        self.status_lbl.configure(text="Running Encodings, please wait...")
        self.train_progress.set(0.1)
        self.update_idletasks()

        trainer = FaceTrainer()
        
        def callback(fraction):
            self.train_progress.set(fraction)
            self.update_idletasks()

        success, msg = trainer.train_model(progress_callback=callback)
        if success:
            self.train_progress.set(1.0)
            self.status_lbl.configure(text="AI Encodings Complete.")
            messagebox.showinfo("Pipeline Success", msg)
        else:
            self.train_progress.set(0)
            self.status_lbl.configure(text="Pipeline Failed.")
            messagebox.showerror("Pipeline Failed", msg)

    # --- 📷 Live Attendance Feed ---
    def start_live_attendance(self):
        recognizer = FaceRecognizer()
        success, msg = recognizer.run_recognition()
        if not success:
            messagebox.showerror("Inference Error", msg)

    # --- 📊 Analytics Screen ---
    def show_analytics(self):
        self.clear_main_frame()
        self.set_nav_active("Analytics")

        analytics_container = ctk.CTkScrollableFrame(self.main_content_frame, fg_color="transparent")
        analytics_container.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            analytics_container, 
            text="Biometric & Attendance Analytics", 
            font=ctk.CTkFont(family="Inter", size=22, weight="bold")
        )
        title.pack(anchor="w", pady=(10, 20))

        # Query Database
        records = self.db.get_attendance_records()
        df = pd.DataFrame(records, columns=["student_id", "name", "date", "time", "status", "confidence"])

        if df.empty:
            no_data = ctk.CTkLabel(
                analytics_container, 
                text="No Attendance records found to render analytics. Mark attendance first.",
                font=ctk.CTkFont(family="Inter", size=14, slant="italic")
            )
            no_data.pack(pady=50)
            return

        df['date'] = pd.to_datetime(df['date'])

        # Graph Frame 1: Daily Attendance Chart
        f1_container = ctk.CTkFrame(analytics_container)
        f1_container.pack(fill="x", pady=10, padx=5)
        
        fig1 = Figure(figsize=(7, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        daily_att = df.groupby(df['date'].dt.date).size()
        ax1.plot(daily_att.index, daily_att.values, marker="o", color="#3498db", linewidth=2)
        ax1.set_title("Attendance Log counts by Date", color="#95a5a6", fontsize=10)
        ax1.tick_params(colors="#95a5a6", labelsize=8)
        self.theme_figure(fig1, ax1)

        canvas1 = FigureCanvasTkAgg(fig1, master=f1_container)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

        # Split Row for Student Performance & Monthly distribution
        row_frame = ctk.CTkFrame(analytics_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=10)
        row_frame.grid_columnconfigure((0, 1), weight=1)

        # Graph 2: Individual Performance (Top 5 Active Students)
        g2_container = ctk.CTkFrame(row_frame)
        g2_container.grid(row=0, column=0, padx=5, sticky="ew")

        fig2 = Figure(figsize=(4.5, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        perf = df['name'].value_counts().head(5)
        ax2.barh(perf.index, perf.values, color="#2ecc71")
        ax2.set_title("Top 5 Active Students (Presence Log)", color="#95a5a6", fontsize=9)
        ax2.tick_params(colors="#95a5a6", labelsize=8)
        self.theme_figure(fig2, ax2)

        canvas2 = FigureCanvasTkAgg(fig2, master=g2_container)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Graph 3: Confidence Distribution Pie Chart
        g3_container = ctk.CTkFrame(row_frame)
        g3_container.grid(row=0, column=1, padx=5, sticky="ew")

        fig3 = Figure(figsize=(4.5, 3), dpi=100)
        ax3 = fig3.add_subplot(111)
        
        # Categorise confidences
        bins = [0, 70, 85, 95, 100]
        labels = ["Fair (<70%)", "Good (70-85%)", "High (85-95%)", "Excellent (>95%)"]
        df['conf_group'] = pd.cut(df['confidence'], bins=bins, labels=labels)
        conf_dist = df['conf_group'].value_counts()

        ax3.pie(conf_dist.values, labels=conf_dist.index, autopct='%1.1f%%', colors=["#e74c3c", "#e67e22", "#3498db", "#2ecc71"], textprops={'color': "#95a5a6", 'fontsize': 8})
        ax3.set_title("AI Recognition Confidence Distribution", color="#95a5a6", fontsize=9)
        self.theme_figure(fig3, ax3)

        canvas3 = FigureCanvasTkAgg(fig3, master=g3_container)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def theme_figure(self, fig, ax):
        bg_color = "#2b2b2b" if self.appearance_mode == "dark" else "#dbdbdb"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

    # --- 📄 Reports & Exports Screen ---
    def show_reports(self):
        self.clear_main_frame()
        self.set_nav_active("Reports")

        reports_container = ctk.CTkFrame(self.main_content_frame)
        reports_container.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            reports_container, 
            text="Attendance Records & Exports", 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#8e44ad"
        )
        title.pack(anchor="w", padx=20, pady=15)

        # Filters Frame
        filters = ctk.CTkFrame(reports_container)
        filters.pack(fill="x", padx=20, pady=10)

        # Student ID Filter
        ctk.CTkLabel(filters, text="ID:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, padx=5, pady=5)
        self.filter_id = ctk.CTkEntry(filters, placeholder_text="Search ID", width=120)
        self.filter_id.grid(row=0, column=1, padx=5, pady=5)

        # Department Filter
        ctk.CTkLabel(filters, text="Dept:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=2, padx=5, pady=5)
        self.filter_dept = ctk.CTkEntry(filters, placeholder_text="Search Dept", width=150)
        self.filter_dept.grid(row=0, column=3, padx=5, pady=5)

        # Date Filter (YYYY-MM-DD)
        ctk.CTkLabel(filters, text="Date (YYYY-MM-DD):", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=4, padx=5, pady=5)
        self.filter_date = ctk.CTkEntry(filters, placeholder_text="YYYY-MM-DD", width=120)
        self.filter_date.grid(row=0, column=5, padx=5, pady=5)

        btn_filter = ctk.CTkButton(
            filters, 
            text="Filter", 
            width=80,
            command=self.populate_reports_table
        )
        btn_filter.grid(row=0, column=6, padx=10, pady=5)

        # Table (Treeview)
        table_frame = ctk.CTkFrame(reports_container)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Styling treeview inside CTk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white", rowheight=25)
        style.configure("Treeview.Heading", background="#1e1e1e", foreground="white", font=("Inter", 10, "bold"))
        style.map("Treeview", background=[('selected', '#3498db')])

        columns = ("StudentID", "Name", "Date", "Time", "Status", "Confidence")
        self.report_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.report_table.heading(col, text=col)
            self.report_table.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.report_table.yview)
        self.report_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.report_table.pack(fill="both", expand=True)

        self.populate_reports_table()

        # Action Buttons (Export)
        export_frame = ctk.CTkFrame(reports_container, fg_color="transparent")
        export_frame.pack(fill="x", padx=20, pady=15)

        btn_csv = ctk.CTkButton(
            export_frame, 
            text="Export CSV", 
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=lambda: self.export_attendance("csv")
        )
        btn_csv.pack(side="left", padx=(0, 15))

        btn_excel = ctk.CTkButton(
            export_frame, 
            text="Export Excel", 
            fg_color="#3498db",
            hover_color="#2980b9",
            command=lambda: self.export_attendance("excel")
        )
        btn_excel.pack(side="left", padx=0)

        btn_email = ctk.CTkButton(
            export_frame, 
            text="Email Last Report", 
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.show_email_panel
        )
        btn_email.pack(side="right", padx=0)

    def populate_reports_table(self):
        # Clear existing items
        for item in self.report_table.get_children():
            self.report_table.delete(item)

        sid = self.filter_id.get().strip() or None
        dept = self.filter_dept.get().strip() or None
        date = self.filter_date.get().strip() or None

        records = self.db.get_attendance_records(date_filter=date, student_id=sid, department=dept)
        for r in records:
            # Format confidence
            conf_str = f"{r[5]:.1f}%" if r[5] else "N/A"
            self.report_table.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], conf_str))

    def export_attendance(self, format_type):
        records = self.db.get_attendance_records()
        df = pd.DataFrame(records, columns=["StudentID", "Name", "Date", "Time", "Status", "Confidence"])
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(base_dir, "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        if format_type == "csv":
            path = os.path.join(reports_dir, "attendance.csv")
            df.to_csv(path, index=False)
            messagebox.showinfo("Exported", f"Successfully exported to reports/attendance.csv")
        else:
            path = os.path.join(reports_dir, "attendance.xlsx")
            df.to_excel(path, index=False)
            messagebox.showinfo("Exported", f"Successfully exported to reports/attendance.xlsx")

    # --- ✉️ Email Automation Frame ---
    def show_email_panel(self):
        email_win = ctk.CTkToplevel(self)
        email_win.title("SMTP Email Report Panel")
        email_win.geometry("450x480")
        email_win.grab_set()

        # Center top level window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (480 // 2)
        email_win.geometry(f"+{x}+{y}")

        title = ctk.CTkLabel(email_win, text="Email Report Automation", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)

        # Inputs
        form_frame = ctk.CTkFrame(email_win, fg_color="transparent")
        form_frame.pack(padx=30, fill="both", expand=True)

        fields = [
            ("SMTP Server:", "smtp_entry", "smtp.gmail.com"),
            ("SMTP Port:", "port_entry", "587"),
            ("Admin Email:", "email_entry", "your_email@gmail.com"),
            ("App Password:", "pass_entry", ""),
            ("Receiver Email:", "dest_entry", "dest_email@gmail.com")
        ]

        entries = {}
        for idx, (lbl_txt, name, default) in enumerate(fields):
            lbl = ctk.CTkLabel(form_frame, text=lbl_txt, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=idx, column=0, padx=10, pady=10, sticky="w")
            
            show_char = "*" if "pass" in name else None
            entry = ctk.CTkEntry(form_frame, placeholder_text=default, show=show_char, width=220)
            entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
            entry.insert(0, default)
            entries[name] = entry

        def send_email():
            smtp_server = entries["smtp_entry"].get().strip()
            port = int(entries["port_entry"].get().strip() or 587)
            sender_email = entries["email_entry"].get().strip()
            password = entries["pass_entry"].get().strip()
            receiver_email = entries["dest_entry"].get().strip()

            if not all([smtp_server, sender_email, password, receiver_email]):
                messagebox.showerror("Error", "Please fill in all email parameters.")
                return

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            report_path = os.path.join(base_dir, "reports", "attendance.xlsx")

            if not os.path.exists(report_path):
                # Try CSV fallback
                report_path = os.path.join(base_dir, "reports", "attendance.csv")
                if not os.path.exists(report_path):
                    messagebox.showerror("Missing file", "Please export the report locally as Excel or CSV before emailing.")
                    return

            try:
                # Compose Email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = f"SmartAttend AI Attendance Report - {datetime.now().strftime('%Y-%m-%d')}"

                body = "Hello Administrator,\n\nPlease find attached the latest attendance export compiled from SmartAttend AI."
                msg.attach(MIMEText(body, 'plain'))

                # Attach file
                with open(report_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(report_path)}")
                    msg.attach(part)

                # Send
                server = smtplib.SMTP(smtp_server, port)
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
                server.quit()

                messagebox.showinfo("Sent Success", "Attendance report emailed successfully!")
                email_win.destroy()
            except Exception as e:
                logging.error(f"Failed to email report: {e}")
                messagebox.showerror("Email Error", f"Failed to send email:\n{str(e)}")

        btn_send = ctk.CTkButton(email_win, text="Send Email Now", fg_color="#2ecc71", hover_color="#27ae60", command=send_email)
        btn_send.pack(pady=20)

    # --- ⚙ Settings Panel ---
    def show_settings(self):
        self.clear_main_frame()
        self.set_nav_active("Settings")

        settings_container = ctk.CTkFrame(self.main_content_frame)
        settings_container.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            settings_container, 
            text="System Settings", 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#7f8c8d"
        )
        title.pack(anchor="w", padx=30, pady=(30, 20))

        # Config layout
        grid = ctk.CTkFrame(settings_container, fg_color="transparent")
        grid.pack(anchor="w", padx=30, pady=10)

        # Recognition Threshold slider
        ctk.CTkLabel(grid, text="Recognition Confidence Threshold:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, padx=(0, 20), pady=15, sticky="w")
        self.thresh_slider = ctk.CTkSlider(grid, from_=40, to=90, width=200)
        self.thresh_slider.grid(row=0, column=1, pady=15, sticky="w")
        self.thresh_slider.set(60) # default match threshold (0.6 dist -> 60% confidence)

        # Voice Assistant Feedback switch
        ctk.CTkLabel(grid, text="Voice Synthesizer Feedback:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, padx=(0, 20), pady=15, sticky="w")
        self.voice_switch = ctk.CTkSwitch(grid, text="Enabled")
        self.voice_switch.grid(row=1, column=1, pady=15, sticky="w")
        self.voice_switch.select()

        # Database maintenance buttons
        ctk.CTkLabel(grid, text="System Maintenance:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, padx=(0, 20), pady=15, sticky="w")
        btn_clear_cache = ctk.CTkButton(
            grid, 
            text="Clean Unknown Faces Directory", 
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.clean_unknown_dir
        )
        btn_clear_cache.grid(row=2, column=1, pady=15, sticky="w")

        # Save Button
        btn_save = ctk.CTkButton(
            settings_container, 
            text="Save Configuration", 
            fg_color="#3498db",
            hover_color="#2980b9",
            command=lambda: messagebox.showinfo("Saved", "System configurations applied.")
        )
        btn_save.pack(anchor="w", padx=30, pady=30)

    def clean_unknown_dir(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        unknown_dir = os.path.join(base_dir, "unknown_faces")
        if os.path.exists(unknown_dir):
            for file in os.listdir(unknown_dir):
                os.remove(os.path.join(unknown_dir, file))
            messagebox.showinfo("Maintenance", "Cleaned unknown_faces/ cache folder successfully.")
        else:
            messagebox.showinfo("Maintenance", "Cache directory empty.")
