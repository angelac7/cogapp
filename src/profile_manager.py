import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime

class ProfileManager:
    def __init__(self, parent, colors, fonts):
        self.parent = parent
        self.colors = colors
        self.fonts = fonts
        self.current_frame = None
        self.user_data = self.load_user_data()

    def load_user_data(self):
        default_data = {
            "username": "User",
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "goals": [],
            "support_tickets": []
        }
        try:
            if os.path.exists('user_profile.json'):
                with open('user_profile.json', 'r') as f:
                    return json.load(f)
            return default_data
        except:
            return default_data
            
    def save_user_data(self):
        with open('user_profile.json', 'w') as f:
            json.dump(self.user_data, f)

    def create_profile_page(self, main_frame):
        if self.current_frame:
            self.current_frame.destroy()       
        self.current_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['background'])
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)
        self.current_frame.grid_rowconfigure(1, weight=1)
        
        nav_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        nav_frame.grid_columnconfigure((0,1), weight=1)
        
        sections = ["Profile", "Support"]
        self.nav_buttons = {}
        
        for i, section in enumerate(sections):
            btn = ctk.CTkButton(
                nav_frame,
                text=section,
                font=self.fonts['button'],
                fg_color=self.colors['surface'],
                hover_color=self.colors['primary'],
                text_color=self.colors['text'],
                command=lambda s=section: self.switch_section(s)
            )
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            self.nav_buttons[section] = btn
        
        self.content_frame = ctk.CTkFrame(self.current_frame, fg_color=self.colors['surface'])
        self.content_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.show_profile_section()

    def switch_section(self, section):
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == section:
                btn.configure(fg_color=self.colors['primary'])
            else:
                btn.configure(fg_color=self.colors['surface'])
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if section == "Profile":
            self.show_profile_section()
        elif section == "Support":
            self.show_support_section()

    def show_profile_section(self):
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)
        main_container.grid_columnconfigure((0,1), weight=1)
        
        left_column = ctk.CTkFrame(main_container, fg_color=self.colors['background'])
        left_column.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        username_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        username_frame.pack(fill="x", pady=20, padx=20)
        
        self.username_label = ctk.CTkLabel(
            username_frame,
            text=self.user_data['username'],
            font=self.fonts['heading'],
            text_color=self.colors['text']
        )
        self.username_label.pack(side="left")
        
        edit_btn = ctk.CTkButton(
            username_frame,
            text="✏️",
            width=30,
            font=self.fonts['body'],
            fg_color="transparent",
            hover_color=self.colors['accent'],
            command=self.edit_username
        )
        edit_btn.pack(side="left", padx=10)
        
        joined_label = ctk.CTkLabel(
            left_column,
            text=f"Member since: {self.user_data['joined_date']}",
            font=self.fonts['body'],
            text_color=self.colors['subtext']
        )
        joined_label.pack(pady=10, padx=20, anchor="w")
        
        right_column = ctk.CTkFrame(main_container, fg_color=self.colors['background'])
        right_column.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        goals_header = ctk.CTkFrame(right_column, fg_color="transparent")
        goals_header.pack(fill="x", pady=10, padx=20)
        
        goals_title = ctk.CTkLabel(
            goals_header,
            text="Goals",
            font=self.fonts['subheading'],
            text_color=self.colors['accent']
        )
        goals_title.pack(side="left")
        
        add_goal_btn = ctk.CTkButton(
            goals_header,
            text="+ New Goal",
            font=self.fonts['body'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            command=self.add_goal_dialog
        )
        add_goal_btn.pack(side="right")
        
        self.show_goals_list(right_column)

    def show_goals_list(self, parent_frame):
        goals_list = ctk.CTkScrollableFrame(
            parent_frame,
            fg_color="transparent",
            height=400
        )
        goals_list.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        if 'goals' in self.user_data and self.user_data['goals']:
            for goal in self.user_data['goals']:
                self.create_goal_item(goals_list, goal)
        else:
            no_goals = ctk.CTkLabel(
                goals_list,
                text="Set your first goal to start tracking progress!",
                font=self.fonts['body'],
                text_color=self.colors['subtext']
            )
            no_goals.pack(pady=20)

    def create_goal_item(self, parent_frame, goal):
        goal_frame = ctk.CTkFrame(
            parent_frame,
            fg_color=self.colors['surface']
        )
        goal_frame.pack(fill="x", pady=5)
        
        goal_header = ctk.CTkFrame(goal_frame, fg_color="transparent")
        goal_header.pack(fill="x", padx=10, pady=5)
        
        status_color = self.colors['accent'] if goal['completed'] else self.colors['text']
        status_text = "✓" if goal['completed'] else "○"
        
        status_btn = ctk.CTkButton(
            goal_header,
            text=status_text,
            width=30,
            font=self.fonts['body'],
            fg_color="transparent",
            hover_color=self.colors['accent'],
            text_color=status_color,
            command=lambda: self.toggle_goal_status(goal)
        )
        status_btn.pack(side="left", padx=5)
        
        goal_text = ctk.CTkLabel(
            goal_header,
            text=goal['description'],
            font=self.fonts['body'],
            text_color=status_color
        )
        goal_text.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            goal_header,
            text="🗑️",
            width=30,
            font=self.fonts['body'],
            fg_color="transparent",
            hover_color="#FF4444",
            command=lambda: self.delete_goal(goal)
        )
        delete_btn.pack(side="right", padx=5)
        
        goal_details = ctk.CTkLabel(
            goal_frame,
            text=f"Target Date: {goal['target_date']}",
            font=self.fonts['body'],
            text_color=self.colors['subtext']
        )
        goal_details.pack(padx=10, pady=5)

    def add_goal_dialog(self):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Add New Goal")
        dialog.geometry("400x300")
        dialog.configure(fg_color=self.colors['background'])
        
        frame = ctk.CTkFrame(dialog, fg_color=self.colors['surface'])
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="Set New Goal",
            font=self.fonts['subheading'],
            text_color=self.colors['accent']
        )
        title.pack(pady=10)
        
        description = ctk.CTkEntry(
            frame,
            placeholder_text="Goal description",
            font=self.fonts['body'],
            height=40,
            width=300
        )
        description.pack(pady=10)
        
        date_frame = self.create_date_picker(frame)
        
        save_btn = ctk.CTkButton(
            frame,
            text="Save Goal",
            font=self.fonts['button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            command=lambda: self.save_goal(
                description.get(),
                f"{date_frame['year'].get()}-{date_frame['month'].get()}-{date_frame['day'].get()}",
                dialog
            )
        )
        save_btn.pack(pady=20)

    def create_date_picker(self, parent_frame):
        date_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        date_frame.pack(pady=10)
        
        months = [str(i).zfill(2) for i in range(1, 13)]
        days = [str(i).zfill(2) for i in range(1, 32)]
        years = [str(datetime.now().year + i) for i in range(3)]
        
        month_menu = ctk.CTkOptionMenu(
            date_frame,
            values=months,
            font=self.fonts['body'],
            fg_color=self.colors['surface']
        )
        month_menu.pack(side="left", padx=5)
        
        day_menu = ctk.CTkOptionMenu(
            date_frame,
            values=days,
            font=self.fonts['body'],
            fg_color=self.colors['surface']
        )
        day_menu.pack(side="left", padx=5)
        
        year_menu = ctk.CTkOptionMenu(
            date_frame,
            values=years,
            font=self.fonts['body'],
            fg_color=self.colors['surface']
        )
        year_menu.pack(side="left", padx=5)
        
        return {
            'month': month_menu,
            'day': day_menu,
            'year': year_menu
        }

    def save_goal(self, description, target_date, dialog):
        if not description:
            messagebox.showwarning("Warning", "Please enter a goal description")
            return
            
        if 'goals' not in self.user_data:
            self.user_data['goals'] = []
            
        goal = {
            'description': description,
            'target_date': target_date,
            'completed': False,
            'date_added': datetime.now().strftime("%Y-%m-%d")
        }
        
        self.user_data['goals'].append(goal)
        self.save_user_data()
        dialog.destroy()
        self.switch_section("Profile")

    def toggle_goal_status(self, goal):
        goal['completed'] = not goal['completed']
        self.save_user_data()
        self.show_profile_section()

    def delete_goal(self, goal):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this goal?"):
            if goal in self.user_data['goals']:
                self.user_data['goals'].remove(goal)
                self.save_user_data()
                self.switch_section("Profile")

    def edit_username(self):
        dialog = ctk.CTkInputDialog(
            text="Enter new username:",
            title="Edit Username",
            button_fg_color=self.colors['primary'],
            button_hover_color=self.colors['accent']
        )
        new_username = dialog.get_input()
        if new_username and new_username.strip():
            self.user_data['username'] = new_username
            self.username_label.configure(text=new_username)
            self.save_user_data()
            messagebox.showinfo("Success", "Username updated successfully!")

    def show_support_section(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        support_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        support_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        new_ticket_frame = ctk.CTkFrame(support_frame, fg_color=self.colors['background'])
        new_ticket_frame.pack(fill="x", expand=False, pady=(0, 20))
        
        title = ctk.CTkLabel(
            new_ticket_frame,
            text="Support Center",
            font=self.fonts['heading'],
            text_color=self.colors['accent']
        )
        title.pack(pady=20)
        
        ticket_frame = ctk.CTkFrame(new_ticket_frame, fg_color=self.colors['surface'])
        ticket_frame.pack(fill="x", pady=10, padx=40)
        
        new_ticket_label = ctk.CTkLabel(
            ticket_frame,
            text="Submit New Ticket",
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        )
        new_ticket_label.pack(pady=10)
        
        categories = ["Technical Issue", "Account Help", "Feature Request", "Bug Report", "Other"]
        category_var = ctk.StringVar(value=categories[0])
        
        category_menu = ctk.CTkOptionMenu(
            ticket_frame,
            values=categories,
            variable=category_var,
            font=self.fonts['body'],
            fg_color=self.colors['background'],
            button_color=self.colors['primary'],
            button_hover_color=self.colors['accent']
        )
        category_menu.pack(pady=10)
        
        subject_entry = ctk.CTkEntry(
            ticket_frame, placeholder_text="Subject",
            font=self.fonts['body'],
            height=40
        )
        subject_entry.pack(pady=10, padx=20, fill="x")
        
        message_text = ctk.CTkTextbox(
            ticket_frame,
            font=self.fonts['body'],
            height=100,
            fg_color=self.colors['background']
        )
        message_text.pack(pady=20, padx=20, fill="x")
        
        submit_btn = ctk.CTkButton(
            ticket_frame,
            text="Submit Ticket",
            font=self.fonts['button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            command=lambda: self.submit_support_ticket(
                category_var.get(),
                subject_entry.get(),
                message_text.get("1.0", "end-1c")
            )
        )
        submit_btn.pack(pady=20)

        history_frame = ctk.CTkFrame(support_frame, fg_color=self.colors['background'])
        history_frame.pack(fill="both", expand=True)
        
        history_label = ctk.CTkLabel(
            history_frame,
            text="Ticket History",
            font=self.fonts['subheading'],
            text_color=self.colors['text']
        )
        history_label.pack(pady=10)
        
        tickets_container = ctk.CTkScrollableFrame(
            history_frame,
            fg_color=self.colors['surface'],
            height=300
        )
        tickets_container.pack(fill="both", expand=True, padx=40, pady=10)
        
        if self.user_data.get('support_tickets'):
            for ticket in reversed(self.user_data['support_tickets']):
                ticket_item = ctk.CTkFrame(tickets_container, fg_color=self.colors['background'])
                ticket_item.pack(fill="x", pady=5)
                
                header_frame = ctk.CTkFrame(ticket_item, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=5)
                
                status_color = "#4CAF50" if ticket['status'] == 'Open' else "#FF9800"
                ctk.CTkLabel(
                    header_frame,
                    text="●",
                    font=self.fonts['body'],
                    text_color=status_color,
                    width=20
                ).pack(side="left")
                
                ctk.CTkLabel(
                    header_frame,
                    text=ticket['subject'],
                    font=self.fonts['body'],
                    text_color=self.colors['accent']
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    header_frame,
                    text=ticket['date'],
                    font=self.fonts['body'],
                    text_color=self.colors['subtext']
                ).pack(side="right")
                
                details_frame = ctk.CTkFrame(ticket_item, fg_color="transparent")
                details_frame.pack(fill="x", padx=10, pady=(0, 5))
                
                ctk.CTkLabel(
                    details_frame,
                    text=f"Category: {ticket['category']}",
                    font=self.fonts['body'],
                    text_color=self.colors['text']
                ).pack(side="left")
                
                ctk.CTkLabel(
                    details_frame,
                    text=f"Status: {ticket['status']}",
                    font=self.fonts['body'],
                    text_color=self.colors['text']
                ).pack(side="right")
        else:
            ctk.CTkLabel(
                tickets_container,
                text="No support tickets yet",
                font=self.fonts['body'],
                text_color=self.colors['subtext']
            ).pack(pady=20)

    def submit_support_ticket(self, category, subject, message):
        if not subject or not message:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
            
        if 'support_tickets' not in self.user_data:
            self.user_data['support_tickets'] = []
            
        ticket = {
            'category': category,
            'subject': subject,
            'message': message,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Open'
        }
        
        self.user_data['support_tickets'].append(ticket)
        self.save_user_data()
        messagebox.showinfo("Success", "Support ticket submitted successfully")
        self.switch_section("Support")