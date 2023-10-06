from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from random import shuffle



class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.label = Label(text="Welcome to Zux Quiz App", font_size=24)
        self.start_button = Button(text="Start Quiz", on_press=self.start_quiz, size_hint=(None, None))
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def start_quiz(self, instance):
        self.manager.current = "quiz"


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Mars", "Venus", "Jupiter", "Saturn"],
                "correct_answer": "Mars"
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct_answer": "Blue Whale"
            }
        ]

        self.shuffle_questions()  # Shuffle the questions at the start

        self.layout = BoxLayout(orientation="vertical")

        self.question_index = 0
        self.score = 0

        self.question_label = Label(text="")
        self.layout.add_widget(self.question_label)

        self.options_layout = GridLayout(cols=2)
        self.layout.add_widget(self.options_layout)

        self.next_button = Button(text="Next Question", on_press=self.next_question)
        self.layout.add_widget(self.next_button)

        self.score_label = Label(text="Score: 0", size_hint_y=None, height=44)
        self.layout.add_widget(self.score_label)

        self.progress_label = Label(text=f"Question {self.question_index + 1} of {len(self.questions)}",
                                    size_hint_y=None, height=44)
        self.layout.add_widget(self.progress_label)

        self.timer_label = Label(text="Time Left: 10", size_hint_y=None, height=44)
        self.layout.add_widget(self.timer_label)

        self.feedback_label = Label(text="", size_hint_y=None, height=44)
        self.layout.add_widget(self.feedback_label)

        self.menu_button = Button(text="Main Menu", on_press=self.goto_menu, size_hint_y=None, height=44)
        self.layout.add_widget(self.menu_button)

        self.restart_button = Button(text="Restart Quiz", on_press=self.restart_quiz, size_hint_y=None, height=44)
        self.restart_button.disabled = True
        self.layout.add_widget(self.restart_button)

        self.start_timer()

        self.load_question()
        self.add_widget(self.layout)

    def shuffle_questions(self):
        shuffle(self.questions)

    def start_timer(self):
        self.time_left = 10
        self.timer_label.text = f"Time Left: {self.time_left}"
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time Left: {self.time_left}"
        if self.time_left <= 0:
            self.next_question(None)  # Move to the next question when time is up

    def load_question(self):
        if self.question_index < len(self.questions):
            question = self.questions[self.question_index]
            self.question_label.text = f"Question {self.question_index + 1}: {question['question']}"
            self.options_layout.clear_widgets()
            options = question["options"]
            shuffle(options)
            for option in options:
                btn = ToggleButton(text=option, group="options")
                self.options_layout.add_widget(btn)
            self.reset_timer()  # Reset the timer for each new question
            self.progress_label.text = f"Question {self.question_index + 1} of {len(self.questions)}"
            self.feedback_label.text = ""  # Clear previous feedback
        else:
            self.question_label.text = f"Quiz Completed! Score: {self.score}/{len(self.questions)}"
            self.next_button.disabled = True
            self.restart_button.disabled = False
            Clock.unschedule(self.timer_event)  # Stop the timer

    def reset_timer(self):
        self.time_left = 10
        self.timer_label.text = f"Time Left: {self.time_left}"

    def next_question(self, instance):
        if self.question_index < len(self.questions):
            question = self.questions[self.question_index]
            selected_option = None
            for child in self.options_layout.children:
                if child.state == "down":
                    selected_option = child.text
            if selected_option == question["correct_answer"]:
                self.score += 1
                self.feedback_label.text = "Correct!"
            else:
                self.feedback_label.text = "Incorrect."
            self.question_index += 1
            self.score_label.text = f"Score: {self.score}"
            self.load_question()
        else:
            self.load_question()

    def restart_quiz(self, instance):
        self.question_index = 0
        self.score = 0
        self.shuffle_questions()  # Shuffle questions for a new quiz session
        self.start_timer()
        self.next_button.disabled = False
        self.restart_button.disabled = True
        self.score_label.text = "Score: 0"
        self.load_question()

    def goto_menu(self, instance):
        self.manager.current = "welcome"


class QuizApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.welcome_screen = WelcomeScreen(name="welcome")
        self.quiz_screen = QuizScreen(name="quiz")
        self.sm.add_widget(self.welcome_screen)
        self.sm.add_widget(self.quiz_screen)
        return self.sm


if __name__ == '__main__':
    QuizApp().run()
