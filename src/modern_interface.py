import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import time
from datetime import datetime
from src.exercise_manager import ExerciseManager
from src.database_manager import DatabaseManager
from src.profile_manager import ProfileManager
from src.medication_manager import MedicationManager

class ModernCogniCore:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CogniCore")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.db = DatabaseManager()
        self.exercise_manager = ExerciseManager()
        self.colors = {
            'primary': '#0052CC', 'secondary': '#091E42', 'accent': '#00B8D9',
            'highlight': '#4C9AFF', 'background': '#0A1929', 'surface': '#112236',
            'text': '#FFFFFF', 'subtext': '#A6B1BB'
        }
        self.fonts = {
            'display': ('Darker Grotesque', 64, 'bold'),
            'heading': ('Darker Grotesque', 32, 'bold'),
            'subheading': ('Gruppo', 24, 'normal'),
            'body': ('Gruppo', 16, 'normal'),
            'button': ('Darker Grotesque', 18, 'bold')
        }
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.create_navigation()
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['background'])
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.profile_manager = None
        self.medication_manager = None
        self.show_welcome_screen()

    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self.root, height=80, fg_color=self.colors['surface'])
        nav_frame.grid(row=0, column=0, sticky="ew")
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_propagate(False)
        
        logo_btn = self._create_button(nav_frame, "COGNICORE", self.show_welcome_screen,
            ('Darker Grotesque', 24, 'bold'), "transparent", self.colors['accent'])
        logo_btn.grid(row=0, column=0, padx=30, pady=20)
        
        btn_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e", padx=30)
        
        for text, cmd in [("EXERCISES", self.show_categories), ("PROGRESS", self.show_progress),
                         ("PROFILE", self.show_profile), ("MEDS", self.show_medications)]:
            self._create_button(btn_frame, text, cmd, ('Gruppo', 16, 'bold'), 
                "transparent", self.colors['text'], width=120, height=40).pack(side="left", padx=10)

    def _create_button(self, parent, text, command, font=None, fg_color=None, text_color=None, **kwargs):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=font or self.fonts['button'],
            fg_color=fg_color or self.colors['primary'],
            text_color=text_color or self.colors['text'],
            hover_color=kwargs.pop('hover_color', self.colors['accent']),
            **kwargs
        )

    def _create_label(self, parent, text, font, color=None, **kwargs):
        return ctk.CTkLabel(parent, text=text, font=font, 
            text_color=color or self.colors['text'], **kwargs)

    def show_welcome_screen(self):
        self._clear_frame(self.main_frame)
        welcome_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['background'])
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid_columnconfigure(0, weight=1)
        welcome_frame.grid_rowconfigure((0, 1), weight=1)
        
        content_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=(40, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        
        self._create_label(content_frame, "TRAIN YOUR MIND", self.fonts['display'], 
            self.colors['accent']).pack(pady=(20, 10))
        self._create_label(content_frame, "BUILD LASTING HABITS", self.fonts['heading'], 
            self.colors['highlight']).pack(pady=(10, 20))
        self._create_label(content_frame, "Challenge yourself with cognitive exercises designed to enhance your mental capabilities",
            self.fonts['subheading'], self.colors['subtext'], wraplength=800).pack(pady=(0, 30))
        
        self._create_button(content_frame, "START", self.show_categories, self.fonts['button'],
            self.colors['primary'], self.colors['text'], width=300, height=60).pack(pady=(60, 80))
        
        features_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        features_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=(20, 40))
        features_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        features = [("🧠 Adaptive\nTraining", "Exercises that evolve with your progress"),
                   ("📊 Performance\nTracking", "Monitor your cognitive growth"),
                   ("🎯 Personalized\nGoals", "Set and achieve your targets")]
        
        for i, (title, desc) in enumerate(features):
            frame = ctk.CTkFrame(features_frame, fg_color=self.colors['surface'])
            frame.grid(row=0, column=i, padx=10, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure((0, 1), weight=1)
            self._create_label(frame, title, self.fonts['subheading'], 
                self.colors['accent']).pack(expand=True, pady=(30, 0))
            self._create_label(frame, desc, self.fonts['body'], 
                self.colors['subtext'], wraplength=250).pack(expand=True, pady=(0, 30), padx=20)

    def show_categories(self):
        self._clear_frame(self.main_frame)
        categories_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['background'])
        categories_frame.grid(row=0, column=0, sticky="nsew")
        categories_frame.grid_columnconfigure((0,1), weight=1)
        categories_frame.grid_rowconfigure((1,2), weight=1)
        
        self._create_label(categories_frame, "SELECT YOUR CHALLENGE", self.fonts['heading'],
            self.colors['accent']).grid(row=0, column=0, columnspan=2, pady=(40,30))
        
        categories = [("MEMORY", "Enhance your recall abilities", '#1E3A8A', '#2563EB'),
                     ("LOGIC", "Master problem-solving skills", '#1E40AF', '#3B82F6'),
                     ("FOCUS", "Sharpen your attention", '#1D4ED8', '#60A5FA'),
                     ("SPEED", "Boost your mental agility", '#2563EB', '#93C5FD')]
        
        for idx, (cat, desc, bg_color, btn_color) in enumerate(categories):
            frame = ctk.CTkFrame(categories_frame, fg_color=bg_color, corner_radius=15)
            frame.grid(row=1 if idx < 2 else 2, column=idx % 2, sticky="nsew", padx=20, pady=20)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure((0,1,2), weight=1)
            
            self._create_label(frame, cat, self.fonts['heading']).grid(row=0, column=0, pady=(40,10))
            self._create_label(frame, desc, self.fonts['body'], 
                self.colors['subtext']).grid(row=1, column=0, pady=10)
            
            diff_frame = ctk.CTkFrame(frame, fg_color="transparent")
            diff_frame.grid(row=2, column=0, pady=(20,40))
            
            for diff in ['EASY', 'MEDIUM', 'HARD']:
                self._create_button(diff_frame, diff, lambda c=cat, d=diff: self.start_exercise(c, d.lower()),
                    self.fonts['button'], btn_color, self.colors['text'], width=100, height=35,
                    corner_radius=8).pack(side="left", padx=5)

    def _clear_frame(self, frame):
        for widget in frame.winfo_children(): widget.destroy()

    def start_exercise(self, category, difficulty):
        exercise = self.exercise_manager.get_exercise(category, difficulty)
        if not exercise:
            messagebox.showerror("Error", "No exercise available")
            return
        
        exercise_window = ctk.CTkToplevel(self.root)
        exercise_window.title(f"CogniCore - {category}")
        exercise_window.geometry("800x600")
        exercise_window.configure(fg_color=self.colors['background'])
        exercise_window.grid_columnconfigure(0, weight=1)
        exercise_window.grid_rowconfigure(0, weight=1)
        
        frame = ctk.CTkFrame(exercise_window, fg_color=self.colors['surface'])
        frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=20)
        header_frame.grid_columnconfigure(1, weight=1)
        
        self._create_button(header_frame, "← Back", exercise_window.destroy,
            self.fonts['body'], "transparent", self.colors['text'], 
            width=80).grid(row=0, column=0, padx=20)
            
        self._create_label(header_frame, f"{category} - {difficulty.upper()}", 
            self.fonts['heading'], self.colors['accent']).grid(row=0, column=1)
            
        self._create_label(frame, exercise['question'], self.fonts['subheading'], 
            wraplength=600).grid(row=1, column=0, pady=30)
            
        self._create_label(frame, exercise['instruction'], self.fonts['body'], 
            self.colors['subtext']).grid(row=2, column=0, pady=10)
        
        answer_var = tk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=answer_var, font=self.fonts['body'],
            width=300, height=50, fg_color=self.colors['background'],
            border_color=self.colors['accent'])
        entry.grid(row=3, column=0, pady=30)
        
        timer_label = self._create_label(frame, str(exercise.get('time_limit', 30)),
            self.fonts['subheading'], self.colors['highlight'])
        timer_label.grid(row=4, column=0, pady=10)
        
        self._create_button(frame, "SUBMIT", 
            lambda: self.submit_answer(exercise, answer_var.get(), exercise_window),
            self.fonts['button'], self.colors['primary'], self.colors['text'],
            width=200, height=50).grid(row=5, column=0, pady=30)
        
        entry.focus_set()
        self.start_timer(exercise_window, timer_label, exercise.get('time_limit', 30))

    def start_timer(self, window, label, time_left):
        if time_left > 0:
            label.configure(text=f"Time remaining: {time_left}s")
            window.after(1000, lambda: self.start_timer(window, label, time_left - 1))
        else:
            label.configure(text="Time's up!")
            window.after(1000, window.destroy)

    def submit_answer(self, exercise, answer, window):
        is_correct = self.exercise_manager.check_answer(exercise, answer)
        score = self.exercise_manager.calculate_score(is_correct, 
            exercise.get('time_limit', 30), exercise.get('time_limit', 30))
            
        self.db.save_result(exercise['category'], exercise['difficulty'],
            score, exercise.get('time_limit', 30), is_correct)
            
        result_window = ctk.CTkToplevel(self.root)
        result_window.title("Result")
        result_window.geometry("400x300")
        result_window.configure(fg_color=self.colors['background'])
        
        result_frame = ctk.CTkFrame(result_window, fg_color=self.colors['surface'])
        result_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_label(result_frame, "CORRECT!" if is_correct else "INCORRECT",
            self.fonts['heading'], 
            self.colors['accent'] if is_correct else self.colors['primary']).pack(pady=20)
            
        self._create_label(result_frame, f"Score: {score}",
            self.fonts['subheading']).pack(pady=10)
            
        self._create_label(result_frame, self.exercise_manager.get_feedback(score),
            self.fonts['body'], self.colors['subtext']).pack(pady=20)
            
        self._create_button(result_frame, "CONTINUE",
            lambda: [result_window.destroy(), window.destroy()],
            self.fonts['button'], self.colors['primary'],
            self.colors['text']).pack(pady=20)
            
        window.withdraw()

    def show_progress(self):
        self._clear_frame(self.main_frame)
        progress_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['background'])
        progress_frame.grid(sticky="nsew", padx=40, pady=40)
        progress_frame.grid_columnconfigure(0, weight=1)
    
        header_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        header_frame.grid_columnconfigure(1, weight=1)
    
        self._create_label(header_frame, "YOUR PROGRESS",
            self.fonts['heading'], self.colors['accent']).grid(row=0, column=1, pady=(0, 30))
    
        
        stats = self.db.get_statistics()
        if stats:
            overall_frame = ctk.CTkFrame(progress_frame, fg_color=self.colors['surface'])
            overall_frame.grid(row=1, column=0, sticky="ew", pady=20)
            overall_frame.grid_columnconfigure((0,1,2,3), weight=1)
            
            total_exercises, avg_score, total_correct, avg_time = stats
            success_rate = (total_correct / total_exercises * 100) if total_exercises else 0
            
            stat_titles = ["Total Exercises", "Average Score", "Success Rate", "Avg Time (s)"]
            stat_values = [
                total_exercises or 0,
                f"{avg_score:.1f}" if avg_score else "0.0",
                f"{success_rate:.1f}%",
                f"{avg_time:.1f}" if avg_time else "0.0"
            ]
            
            for i, (title, value) in enumerate(zip(stat_titles, stat_values)):
                stat_box = ctk.CTkFrame(overall_frame, fg_color=self.colors['background'])
                stat_box.grid(row=0, column=i, padx=10, pady=20, sticky="ew")
                self._create_label(stat_box, str(value), self.fonts['heading'],
                    self.colors['accent']).pack(pady=(20,5))
                self._create_label(stat_box, title, self.fonts['body'],
                    self.colors['subtext']).pack(pady=(5,20))

        history_frame = ctk.CTkScrollableFrame(progress_frame,
            fg_color=self.colors['surface'], height=400)
        history_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        progress_frame.grid_rowconfigure(2, weight=1)
        
        self._create_label(history_frame, "Exercise History",
            self.fonts['subheading']).pack(pady=20)
        
        history = self.db.get_progress_data()
        if history:
            for entry in history:
                entry_frame = ctk.CTkFrame(history_frame, fg_color=self.colors['background'])
                entry_frame.pack(fill="x", padx=20, pady=10)
                
                info_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
                info_frame.pack(side="left", padx=20, pady=10)
                
                self._create_label(info_frame, entry[1], self.fonts['body'],
                    self.colors['accent']).pack(anchor="w")
                self._create_label(info_frame, entry[2].upper(), ('Gruppo', 12, 'normal'),
                    self.colors['subtext']).pack(anchor="w")
                
                stats_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
                stats_frame.pack(side="right", padx=20)
                
                result_text = "✓" if entry[6] else "✗"
                result_color = self.colors['accent'] if entry[6] else "#FF4444"
                
                self._create_label(stats_frame, result_text, self.fonts['body'],
                    result_color).pack(side="right", padx=10)
                self._create_label(stats_frame, f"Score: {entry[3]}", self.fonts['body'],
                    self.colors['text']).pack(side="right", padx=10)
                self._create_label(stats_frame, entry[5], ('Gruppo', 12, 'normal'),
                    self.colors['subtext']).pack(side="right", padx=10)
        else:
            self._create_label(history_frame, "No exercises completed yet",
                self.fonts['body'], self.colors['subtext']).pack(pady=20)

    def show_profile(self):
        self._clear_frame(self.main_frame)
        try:
            if self.profile_manager is None:
                self.profile_manager = ProfileManager(self.main_frame, self.colors, self.fonts)
            self.profile_manager.create_profile_page(self.main_frame)
        except Exception as e:
            print(f"Error loading profile: {e}")
            error_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['background'])
            error_frame.pack(fill="both", expand=True, padx=40, pady=40)
            self._create_label(error_frame, "Profile is currently unavailable",
                self.fonts['heading'], self.colors['accent']).pack(pady=20)
            self._create_button(error_frame, "Retry", self.show_profile,
                self.fonts['button'], self.colors['primary'],
                self.colors['text']).pack(pady=20)

    def show_medications(self):
        self._clear_frame(self.main_frame)
        try:
            if self.medication_manager is None:
                self.medication_manager = MedicationManager(self.main_frame, self.colors, self.fonts)
            self.medication_manager.create_medications_page(self.main_frame)
        except Exception as e:
            print(f"Error loading medications page: {e}")
            error_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['background'])
            error_frame.pack(fill="both", expand=True, padx=40, pady=40)
            self._create_label(error_frame, "Medications page is currently unavailable",
                self.fonts['heading'], self.colors['accent']).pack(pady=20)
            self._create_button(error_frame, "Retry", self.show_medications,
                self.fonts['button'], self.colors['primary'],
                self.colors['text']).pack(pady=20)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.center_window(self.root, 1200, 800)
        self.root.mainloop()