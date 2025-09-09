import json
import tkinter as tk
from tkinter import simpledialog, messagebox


class QuizBuilder:
    def __init__(self,root):
        self.root = root
        self.root.iconify()

        self.quizData = {
            "name" : "",
            "questions": []
        }

        self.quiz_info()

    def quiz_info(self):
        step = 1
        while(step == 1):
            name = tk.simpledialog.askstring("Quiz Name", "Enter the quiz's name")
            if name == "":
                tk.messagebox.showwarning("Quiz Name","The quiz name should not be empty")
            elif name is None:
                self.root.destroy()
            elif len(name) > 25:
                tk.messagebox.showwarning("Size Not Respected","The name should be 25 characters at most")
            else:
                self.quizData["name"] = name.replace(" ","_").strip()
                step += 1
        while (step == 2):
            self.nb_questions = self.ask_slider(title="Questions Number",prompt="Select the number of questions")
            step+= 1
            self.current_question = 1
            self.get_question()


    def ask_slider(self,title="Select a number", prompt="Choose a value:", 
                   minval=1, maxval=10, initval=1):
        # Create popup
        popup = tk.Toplevel()
        popup.title(title)
        popup.grab_set()  # make it modal (block other windows)

        # Prompt label
        tk.Label(popup, text=prompt).pack(pady=10)

        # Slider widget
        slider = tk.Scale(popup, from_=minval, to=maxval, orient="horizontal")
        slider.set(initval)
        slider.pack(padx=20, pady=10)

        # Variable to store result
        result = {"value": None}

        def on_ok():
            result["value"] = slider.get()
            popup.destroy()

        def on_cancel():
            popup.destroy()

        # Buttons
        tk.Button(popup, text="OK", command=on_ok).pack(side="left", padx=20, pady=10)
        tk.Button(popup, text="Cancel", command=on_cancel).pack(side="right", padx=20, pady=10)

        popup.wait_window()  # Wait until window is closed
        return result["value"]
    
    def get_question(self):
        if self.current_question > self.nb_questions:
            with open(self.quizData["name"]+".json", "w") as f:
                json.dump(self.quizData,f,indent=4)
            return
        questions = {"question" : "", "answers": [], "correct_answer": 0}
        question = self.ask_textarea(f"Question ${self.current_question} :", prompt="Enter the question")
        if question is None:
            tk.messagebox.showwarning("Question Error","The question should not be empty")
            self.get_question()
        questions["question"] = question
        nb_answers = self.ask_slider("Number of Answers","Select the number of the possible answers",maxval=5,minval=1,initval=1)
        answers = []
        for i in range(nb_answers):
            answer = self.ask_textarea(f"Answer ${i+1}", f"Enter the answer no ${i+1} :")
            answers.append(answer)
        questions["answers"] = answers
        correct_answer = self.ask_slider(f"Correct Answer",f"Select the index for the correct answer for the question {self.current_question - 1} : ",maxval=nb_answers -1,minval=0,initval=0)
        questions["correct_answer"] = correct_answer
        self.quizData["questions"].append(questions)
        self.current_question += 1
        self.get_question()

    def ask_textarea(self,title="Input", prompt="Enter your text:"):
        # Create popup window
        popup = tk.Toplevel()
        popup.title(title)
        popup.grab_set()  # Make modal (blocks other windows)

        # Prompt label
        tk.Label(popup, text=prompt).pack(pady=5)

        # Multi-line Text area
        text_area = tk.Text(popup, width=50, height=10, wrap="word")
        text_area.pack(padx=10, pady=5)

        # Variable to store the result
        result = {"value": None}

        def on_ok():
            result["value"] = text_area.get("1.0", tk.END).strip()
            popup.destroy()

        def on_cancel():
            popup.destroy()

        # Buttons
        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side="left", padx=10)

        popup.wait_window()  # Wait until window is closed
        return result["value"]

if __name__ == "__main__":
    root = tk.Tk()
    QuizBuilder(root)

