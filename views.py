# coding: utf-8
DEBUG=False

import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from tkinter import ttk, messagebox
from observer import ConcreteObserver

class StyledFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#f4f6f9", *args, **kwargs)

def configure_styles():
    style = ttk.Style()
    style.configure("TButton",
                    font=("Arial", 11),
                    padding=6)
    style.map("TButton",
              foreground=[("active", "#fff")],
              background=[("active", "#0078D7")])
    
    style.configure("Treeview",
                    font=("Arial", 11),
                    rowheight=28)
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"))

class LoginView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Welcome to QCM App",
                         font=("Helvetica", 18, "bold"),
                         bg="#f4f6f9", fg="#333")
        title.pack(pady=(30, 15))

        user_frame = tk.Frame(self, bg="#f4f6f9")
        user_frame.pack(pady=5)
        tk.Label(user_frame, text="Username:", font=("Arial", 12),
                 bg="#f4f6f9").pack(anchor="w")
        self.username_entry = ttk.Entry(user_frame, width=30)
        self.username_entry.pack()

        pass_frame = tk.Frame(self, bg="#f4f6f9")
        pass_frame.pack(pady=5)
        tk.Label(pass_frame, text="Password:", font=("Arial", 12),
                 bg="#f4f6f9").pack(anchor="w")
        self.password_entry = ttk.Entry(pass_frame, width=30, show="*")
        self.password_entry.pack()

        btn_frame = tk.Frame(self, bg="#f4f6f9")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", command=self.login,
                   width=18).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Register", command=self.register,
                   width=18).grid(row=0, column=1, padx=5)

    def login(self):
        self.controller.login(self.username_entry.get(),
                              self.password_entry.get())

    def register(self):
        self.controller.register(self.username_entry.get(),
                                 self.password_entry.get())


class CreateQuestionsView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller, num_questions, title):
        super().__init__(parent)
        self.controller = controller
        self.num_questions = max(1, int(num_questions))
        self.title = title or "Untitled QCM"
        self.question_frames = []

        tk.Label(self, text=f"Create Questions — {self.title}",
                 font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=12)

        container = tk.Frame(self, bg="#f4f6f9")
        container.pack(fill='both', expand=True, padx=16, pady=(0,10))

        canvas = tk.Canvas(container, bg="#f4f6f9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#f4f6f9")

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i in range(self.num_questions):
            q_block = ttk.Frame(scrollable, padding=(10, 8))
            q_block.pack(fill='x', pady=6)

            ttk.Label(q_block, text=f"Question {i+1}:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")
            q_entry = ttk.Entry(q_block, width=80)
            q_entry.grid(row=1, column=0, columnspan=4, sticky="we", pady=(4,8))

            option_entries = []
            for j in range(4):
                ttk.Label(q_block, text=f"Option {j+1}:", font=("Arial", 10)).grid(row=2 + j, column=0, sticky="w", pady=2)
                opt_entry = ttk.Entry(q_block, width=70)
                opt_entry.grid(row=2 + j, column=1, columnspan=3, sticky="we", padx=(6,0), pady=2)
                option_entries.append(opt_entry)

            ttk.Label(q_block, text="Correct (1-4):", font=("Arial", 10)).grid(row=6, column=0, sticky="w", pady=(6,0))
            correct_var = tk.StringVar(value="1")
            correct_spin = tk.Spinbox(q_block, from_=1, to=4, width=4, textvariable=correct_var)
            correct_spin.grid(row=6, column=1, sticky="w", pady=(6,0))

            self.question_frames.append({
                "question": q_entry,
                "options": option_entries,
                "correct": correct_var
            })

            q_block.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg="#f4f6f9")
        btn_frame.pack(pady=(6,14))

        ttk.Button(btn_frame, text="💾 Save QCM", command=self.save_qcm, width=18).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="⬅ Back", command=self.controller.show_create_qcm, width=18).grid(row=0, column=1, padx=8)

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

            if not q_text:
                messagebox.showwarning("Missing data", f"Question {idx+1} is empty.")
                return
            if any(not opt for opt in opts):
                messagebox.showwarning("Missing data", f"Question {idx+1}: please fill all 4 options.")
                return
            if correct_idx < 0 or correct_idx > 3:
                messagebox.showwarning("Invalid data", f"Question {idx+1}: correct option must be between 1 and 4.")
                return

            questions.append({
                "question": q_text,
                "options": opts,
                "correct": correct_idx
            })

        self.controller.save_qcm(self.title, questions)
        messagebox.showinfo("Saved", f"QCM '{self.title}' saved ({len(questions)} questions).")
        if hasattr(self.controller, "show_qcm_list"):
            self.controller.show_qcm_list()
        else:
            self.controller.show_main_menu()


class MainMenuView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text=f"Hello, {self.controller.get_current_user()} 👋",
                 font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=(30, 15))

        ttk.Button(self, text="▶ Play QCM", command=self.controller.show_qcm_list,
                   width=25).pack(pady=10)
        ttk.Button(self, text="✍ Create QCM", command=self.controller.show_create_qcm,
                   width=25).pack(pady=10)
        ttk.Button(self, text="🚪 Logout", command=self.controller.logout,
                   width=25).pack(pady=10)


class QCMListView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Available QCMs",
                 font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=15)

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

        btn_frame = tk.Frame(self, bg="#f4f6f9")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="▶ Play Selected",
                   command=self.play_selected, width=20).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="⬅ Back",
                   command=self.controller.show_main_menu, width=20).grid(row=0, column=1, padx=8)

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


class CreateQCMView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Create a New QCM",
                 font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=15)

        tk.Label(self, text="QCM Title:", bg="#f4f6f9",
                 font=("Arial", 12)).pack()
        self.title_entry = ttk.Entry(self, width=40)
        self.title_entry.pack(pady=5)

        tk.Label(self, text="Number of Questions:",
                 bg="#f4f6f9", font=("Arial", 12)).pack()
        self.num_questions = tk.Spinbox(self, from_=1, to=50, width=5)
        self.num_questions.pack(pady=5)

        ttk.Button(self, text="Create Questions",
                   command=self.create_questions_frame, width=25).pack(pady=15)
        ttk.Button(self, text="⬅ Back",
                   command=self.controller.show_main_menu, width=25).pack()

    def create_questions_frame(self):
        self.controller.show_create_questions(int(self.num_questions.get()),
                                              self.title_entry.get())


class PlayQCMView(StyledFrame, ConcreteObserver):
    def __init__(self, parent, controller, qcm_title, qcm_id, questions):
        super().__init__(parent)
        self.controller = controller
        self.qcm_title = qcm_title
        self.qcm_id = qcm_id
        self.questions = questions
        self.current_question = 0
        self.answers = []
        self.selected_option = tk.IntVar(value=-1)

        tk.Label(self, text=qcm_title,
                 font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=15)

        self.question_label = tk.Label(self, text="",
                                       font=("Arial", 12),
                                       wraplength=500, bg="#f4f6f9")
        self.question_label.pack(pady=10)

        self.options_frame = tk.Frame(self, bg="#f4f6f9")
        self.options_frame.pack(pady=10)

        self.option_labels = []
        for i in range(4):
            option_frame = tk.Frame(self.options_frame, bg="#f4f6f9")
            option_frame.pack(fill='x', pady=2, padx=20)
            radio_btn = tk.Radiobutton(option_frame, variable=self.selected_option,
                                       value=i, bg="#f4f6f9")
            radio_btn.pack(side='left')
            label = tk.Label(option_frame, text="", wraplength=450,
                             justify='left', font=("Arial", 11), bg="#f4f6f9")
            label.pack(side='left', padx=5)
            self.option_labels.append(label)

        btn_frame = tk.Frame(self, bg="#f4f6f9")
        btn_frame.pack(pady=20)
        self.next_button = ttk.Button(btn_frame, text="Next",
                                      command=self.next_question, width=18)
        self.next_button.grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="Cancel",
                   command=self.controller.show_qcm_list, width=18).grid(row=0, column=1, padx=8)

        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question+1}: {q['question']}")
            self.selected_option.set(-1)
            for i in range(4):
                self.option_labels[i].config(text=q['options'][i] if i < len(q['options']) else "")
            if self.current_question == len(self.questions) - 1:
                self.next_button.config(text="Finish")
            else:
                self.next_button.config(text="Next")

    def next_question(self):
        self.answers.append(self.selected_option.get())
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.calculate_score()

    def calculate_score(self):
        score = sum(1 for i, q in enumerate(self.questions)
                    if self.answers[i] == q['correct'])
        self.controller.save_score(self.qcm_id, score)
        self.controller.show_qcm_list()

    def update(self, subject):
        pass

if   __name__ == "__main__" :
   pass

