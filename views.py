# coding: utf-8
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from observer import ConcreteObserver

ctk.set_appearance_mode("dark")   # "dark", "light", or "system"
ctk.set_default_color_theme("blue")  

class LoginView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")  
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Center container ---
        container = ctk.CTkFrame(self, corner_radius=10)
        container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Login box content ---
        title = ctk.CTkLabel(container, text="🔐 Welcome to QCM App",
                             font=("Segoe UI", 24, "bold"))
        title.pack(pady=(20, 15))

        self.username_entry = ctk.CTkEntry(container, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(container, placeholder_text="Password", show="*", width=280)
        self.password_entry.pack(pady=10)

        ctk.CTkButton(container, text="Login", command=self.login, width=200).pack(pady=15)
        ctk.CTkButton(container, text="Register", command=self.register,
                      width=200, fg_color="gray25", hover_color="gray40").pack()

    def login(self):
        self.controller.login(self.username_entry.get(), self.password_entry.get())

    def register(self):
        self.controller.register(self.username_entry.get(), self.password_entry.get())



class MainMenuView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ctk.CTkLabel(self, text=f"👋 Hello, {self.controller.get_current_user()}",
                             font=("Segoe UI", 22, "bold"))
        title.pack(pady=(40, 30))

        ctk.CTkButton(self, text="▶ Play QCM", command=self.controller.show_qcm_list,
                      width=250).pack(pady=15)
        ctk.CTkButton(self, text="✍ Create QCM", command=self.controller.show_create_qcm,
                      width=250).pack(pady=15)
        ctk.CTkButton(self, text="🚪 Logout", command=self.controller.logout,
                      width=250, fg_color="red3", hover_color="darkred").pack(pady=15)


class QCMListView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller

        ctk.CTkLabel(self, text="📚 Available QCMs",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)
        
        tree_frame = tk.Frame(self, bg="#f4f6f9")
        tree_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(tree_frame,
                                 columns=('ID', 'Title', 'Creator', 'Score'),
                                 show='headings',
                                 yscrollcommand=scrollbar.set)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Creator', text='Creator')
        self.tree.heading('Score', text='Your Score')
        self.tree.column('ID', width=50, anchor="center")
        self.tree.column('Title', width=250)
        self.tree.column('Creator', width=150)
        self.tree.column('Score', width=120, anchor="center")
        self.tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="▶ Play Selected",
                      command=self.play_selected, width=200).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="⬅ Back",
                      command=self.controller.show_main_menu, width=200).grid(row=0, column=1, padx=10)

        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        qcms = self.controller.get_available_qcms()
        for qcm in qcms:
            score = qcm[4] if qcm[4] is not None else "Not played"
            self.tree.insert('', 'end', values=(qcm[0], qcm[1], qcm[3], score))

    def play_selected(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            qcm_id = item['values'][0]
            self.controller.play_qcm(qcm_id)


class CreateQCMView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller

        ctk.CTkLabel(self, text="📝 Create a New QCM",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.title_entry = ctk.CTkEntry(self, placeholder_text="QCM Title", width=300)
        self.title_entry.pack(pady=10)

        self.num_questions = ctk.CTkEntry(self, placeholder_text="Number of Questions", width=300)
        self.num_questions.pack(pady=10)

        ctk.CTkButton(self, text="Create Questions",
                      command=self.create_questions_frame, width=250).pack(pady=15)
        ctk.CTkButton(self, text="⬅ Back",
                      command=self.controller.show_main_menu, width=250).pack()

    def create_questions_frame(self):
        try:
            num = int(self.num_questions.get())
        except ValueError:
            num = 1
        self.controller.show_create_questions(num, self.title_entry.get())


class QuestionsView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller, num_questions, title):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.num_questions = max(1, int(num_questions))
        self.title = title or "Untitled QCM"
        self.question_frames = []

        ctk.CTkLabel(self, text=f"🖊 Create Questions — {self.title}",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, width=700, height=400)
        self.scroll.pack(pady=10)

        for i in range(self.num_questions):
            block = ctk.CTkFrame(self.scroll, corner_radius=8)
            block.pack(fill="x", pady=8, padx=8)

            q_entry = ctk.CTkEntry(block, placeholder_text=f"Question {i+1}", width=600)
            q_entry.pack(pady=5)

            option_entries = []
            for j in range(4):
                opt = ctk.CTkEntry(block, placeholder_text=f"Option {j+1}", width=500)
                opt.pack(pady=3)
                option_entries.append(opt)

            correct_var = ctk.CTkEntry(block, placeholder_text="Correct Option (1-4)", width=150)
            correct_var.pack(pady=5)

            self.question_frames.append({"question": q_entry, "options": option_entries, "correct": correct_var})

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="💾 Save QCM", command=self.save_qcm, width=200).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="⬅ Back", command=self.controller.show_create_qcm, width=200).grid(row=0, column=1, padx=10)

    def save_qcm(self):
        questions = []
        for idx, fr in enumerate(self.question_frames):
            q_text = fr["question"].get().strip()
            opts = [o.get().strip() for o in fr["options"]]
            try:
                correct_idx = int(fr["correct"].get()) - 1
            except Exception:
                messagebox.showwarning("Invalid input", f"Question {idx+1}: correct option must be 1-4.")
                return
            if not q_text or any(not opt for opt in opts) or not (0 <= correct_idx < 4):
                messagebox.showwarning("Invalid data", f"Question {idx+1}: please complete all fields.")
                return
            questions.append({"question": q_text, "options": opts, "correct": correct_idx})

        self.controller.save_qcm(self.title, questions)
        messagebox.showinfo("Saved", f"QCM '{self.title}' saved ({len(questions)} questions).")
        self.controller.show_qcm_list()


class PlayQCMView(ctk.CTkFrame, ConcreteObserver):
    def __init__(self, parent, controller, qcm_title, qcm_id, questions):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.qcm_title = qcm_title
        self.qcm_id = qcm_id
        self.questions = questions
        self.current_question = 0
        self.answers = []
        self.selected_option = ctk.IntVar(value=-1)

        ctk.CTkLabel(self, text=f"🎮 {qcm_title}",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.question_label = ctk.CTkLabel(self, text="", wraplength=600, font=("Segoe UI", 16))
        self.question_label.pack(pady=15)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            rb = ctk.CTkRadioButton(self.options_frame, text="", variable=self.selected_option, value=i)
            rb.pack(anchor="w", pady=5, padx=20)
            self.option_buttons.append(rb)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25)
        self.next_button = ctk.CTkButton(btn_frame, text="Next", command=self.next_question, width=200)
        self.next_button.grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.controller.show_qcm_list, width=200).grid(row=0, column=1, padx=10)

        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.configure(text=f"Question {self.current_question+1}: {q['question']}")
            self.selected_option.set(-1)
            for i, rb in enumerate(self.option_buttons):
                rb.configure(text=q['options'][i] if i < len(q['options']) else "")
            self.next_button.configure(text="Finish" if self.current_question == len(self.questions)-1 else "Next")

    def next_question(self):
        self.answers.append(self.selected_option.get())
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.calculate_score()

    def calculate_score(self):
        score = sum(1 for i, q in enumerate(self.questions) if self.answers[i] == q['correct'])
        self.controller.save_score(self.qcm_id, score)
        self.controller.show_qcm_list()

    def update(self, subject):
        pass


if __name__ == "__main__":
    pass
