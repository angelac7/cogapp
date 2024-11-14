import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime, time
import threading
import platform
from pathlib import Path

class MedicationManager:
    def __init__(self, parent, colors, fonts):
        self.parent = parent
        self.colors = colors
        self.fonts = fonts
        self.current_frame = None
        self.medications_data = self.load_medications_data()
        
    def load_medications_data(self):
        default_data = {"medications": [], "reminders": []}
        try:
            if os.path.exists('medications.json'):
                with open('medications.json', 'r') as f:
                    return json.load(f)
            return default_data
        except:
            return default_data
            
    def save_medications_data(self):
        with open('medications.json', 'w') as f:
            json.dump(self.medications_data, f)

    def create_medications_page(self, main_frame):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)
        self.current_frame.grid_rowconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            self.current_frame,
            text="Medication Tracker",
            font=self.fonts['heading'],
            text_color=self.colors['accent']
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        content_frame = ctk.CTkScrollableFrame(
            self.current_frame,
            fg_color=self.colors['surface']
        )
        content_frame.grid(row=1, column=0, sticky="nsew")
        
        add_frame = ctk.CTkFrame(content_frame, fg_color=self.colors['background'])
        add_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(
            add_frame,
            text="Add New Medication",
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        name_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Medication Name",
            font=self.fonts['body'],
            height=40
        )
        name_entry.pack(pady=5, fill="x")
        
        dosage_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Dosage (e.g., 50mg)",
            font=self.fonts['body'],
            height=40
        )
        dosage_entry.pack(pady=5, fill="x")
        
        frequency_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        frequency_frame.pack(fill="x", pady=5)
        
        times_per_day = ctk.CTkOptionMenu(
            frequency_frame,
            values=["1", "2", "3", "4"],
            font=self.fonts['body'],
            fg_color=self.colors['surface'],
            button_color=self.colors['primary']
        )
        times_per_day.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            frequency_frame,
            text="times per day",
            font=self.fonts['body'],
            text_color=self.colors['subtext']
        ).pack(side="left", padx=5)
        
        notes_text = ctk.CTkTextbox(
            add_frame,
            height=100,
            font=self.fonts['body'],
            fg_color=self.colors['surface']
        )
        notes_text.pack(pady=5, fill="x")
        notes_text.insert("1.0", "Additional notes...")
        
        ctk.CTkButton(
            add_frame,
            text="Add Medication",
            font=self.fonts['button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            command=lambda: self.add_medication(
                name_entry.get(),
                dosage_entry.get(),
                times_per_day.get(),
                notes_text.get("1.0", "end-1c")
            )
        ).pack(pady=10)
        
        meds_frame = ctk.CTkFrame(content_frame, fg_color=self.colors['background'])
        meds_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(
            meds_frame,
            text="Your Medications",
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        ).pack(pady=10)
        
        if self.medications_data['medications']:
            for med in self.medications_data['medications']:
                med_item = ctk.CTkFrame(meds_frame, fg_color=self.colors['surface'])
                med_item.pack(fill="x", pady=5)
                
                header = ctk.CTkFrame(med_item, fg_color="transparent")
                header.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(
                    header,
                    text=f"{med['name']} - {med['dosage']}",
                    font=self.fonts['body'],
                    text_color=self.colors['accent']
                ).pack(side="left")
                
                ctk.CTkButton(
                    header,
                    text="🗑️",
                    width=30,
                    font=self.fonts['body'],
                    fg_color="transparent",
                    hover_color="#FF4444",
                    command=lambda m=med: self.delete_medication(m)
                ).pack(side="right")
                
                ctk.CTkLabel(
                    med_item,
                    text=f"Frequency: {med['frequency']} times per day\nNotes: {med['notes']}",
                    font=self.fonts['body'],
                    text_color=self.colors['subtext']
                ).pack(padx=10, pady=5)
                
                ctk.CTkButton(
                    med_item,
                    text="Set Reminder",
                    font=self.fonts['body'],
                    fg_color=self.colors['primary'],
                    hover_color=self.colors['accent'],
                    command=lambda m=med: self.set_reminder(m)
                ).pack(pady=5)
        else:
            ctk.CTkLabel(
                meds_frame,
                text="No medications added yet",
                font=self.fonts['body'],
                text_color=self.colors['subtext']
            ).pack(pady=20)

    def add_medication(self, name, dosage, frequency, notes):
        if not name or not dosage:
            messagebox.showwarning("Warning", "Please enter medication name and dosage")
            return
            
        medication = {
            'name': name,
            'dosage': dosage,
            'frequency': frequency,
            'notes': notes if notes != "Additional notes..." else "",
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.medications_data['medications'].append(medication)
        self.save_medications_data()
        messagebox.showinfo("Success", "Medication added successfully")
        self.create_medications_page(self.parent)

    def delete_medication(self, medication):
        if messagebox.askyesno("Confirm Delete", f"Delete {medication['name']}?"):
            self.medications_data['medications'].remove(medication)
            self.medications_data['reminders'] = [
                r for r in self.medications_data['reminders']
                if r['medication']['name'] != medication['name']
            ]
            self.save_medications_data()
            self.create_medications_page(self.parent)

    def set_reminder(self, medication):
        window = ctk.CTkToplevel(self.parent)
        window.title(f"Set Reminder - {medication['name']}")
        window.geometry("400x300")
        
        frame = ctk.CTkFrame(window, fg_color=self.colors['background'])
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text=f"Set Reminder for {medication['name']}",
            font=self.fonts['subheading'],
            text_color=self.colors['accent']
        ).pack(pady=10)
        
        time_frame = ctk.CTkFrame(frame, fg_color="transparent")
        time_frame.pack(pady=20)
        
        hours = ctk.CTkOptionMenu(
            time_frame,
            values=[str(i).zfill(2) for i in range(24)],
            font=self.fonts['body'],
            fg_color=self.colors['surface'],
            button_color=self.colors['primary']
        )
        hours.pack(side="left", padx=5)
        
        minutes = ctk.CTkOptionMenu(
            time_frame,
            values=[str(i).zfill(2) for i in range(0, 60, 5)],
            font=self.fonts['body'],
            fg_color=self.colors['surface'],
            button_color=self.colors['primary']
        )
        minutes.pack(side="left", padx=5)
        
        days_frame = ctk.CTkFrame(frame, fg_color="transparent")
        days_frame.pack(pady=20)
        
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_vars = []
        
        for day in days:
            var = ctk.BooleanVar(value=True)
            day_vars.append(var)
            
            ctk.CTkCheckBox(
                days_frame,
                text=day,
                variable=var,
                font=self.fonts['body'],
                fg_color=self.colors['primary']
            ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            frame,
            text="Save Reminder",
            font=self.fonts['button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            command=lambda: self.save_reminder(
                medication,
                hours.get(),
                minutes.get(),
                [day for var, day in zip(day_vars, days) if var.get()],
                window
            )
        ).pack(pady=20)

    def save_reminder(self, medication, hour, minute, days, window):
        reminder = {
            'medication': medication,
            'time': f"{hour}:{minute}",
            'days': days,
            'active': True
        }
        
        self.medications_data['reminders'].append(reminder)
        self.save_medications_data()
        messagebox.showinfo("Success", "Reminder set successfully")
        window.destroy()
        
        self.start_reminder_thread()

    def start_reminder_thread(self):
        def check_reminders():
            while True:
                current_time = datetime.now().time()
                current_day = datetime.now().strftime('%a')
                
                for reminder in self.medications_data['reminders']:
                    if reminder['active']:
                        reminder_time = datetime.strptime(reminder['time'], '%H:%M').time()
                        
                        if (current_time.hour == reminder_time.hour and 
                            current_time.minute == reminder_time.minute and
                            current_day in reminder['days']):
                            
                            if platform.system() == 'Windows':
                                from win10toast import ToastNotifier
                                toaster = ToastNotifier()
                                toaster.show_toast(
                                    "Medication Reminder",
                                    f"Time to take {reminder['medication']['name']} - {reminder['medication']['dosage']}",
                                    duration=10
                                )
                            else:
                                os.system(f"""
                                    osascript -e 'display notification "Time to take {reminder['medication']['name']} - {reminder['medication']['dosage']}" with title "Medication Reminder"'
                                """) 
                import time
                time.sleep(60)
        reminder_thread = threading.Thread(target=check_reminders, daemon=True)
        reminder_thread.start()