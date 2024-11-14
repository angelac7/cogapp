import random
import time
import string
import customtkinter as ctk
from tkinter import messagebox

class ExerciseManager:
    def __init__(self):
        self.category_colors = {
            'MEMORY': {'bg': '#1a237e', 'button': '#3949ab', 'hover': '#283593'},
            'LOGIC': {'bg': '#006064', 'button': '#00838f', 'hover': '#00695c'},
            'FOCUS': {'bg': '#0277bd', 'button': '#039be5', 'hover': '#0277bd'},
            'SPEED': {'bg': '#01579b', 'button': '#0288d1', 'hover': '#01579b'}
        }
        # Exercise definitions for each category and difficulty
        # Structure: category -> difficulty -> list of exercises
        # Each exercise contains: question, possible answers, instruction, time limit
        self.exercises = {
            'MEMORY': {k: [
                {
                    'question': q, 'answer': a, 'instruction': i, 'time_limit': t
                } for q, a, i, t in [
                    ('Remember this sequence:\n7 - 2 - 9 - 4 - 3', 
                     ['72943', '7-2-9-4-3'], 
                     'Enter the numbers with or without dashes', 30),
                    ('Memorize these colors:\nBLUE → GOLD → RED → GREEN',
                     ['blue gold red green', 'BLUE GOLD RED GREEN', 'Blue Gold Red Green'],
                     'Type the colors in order', 30)
                ]
            ] for k in ['easy']}
        }
        self.exercises['MEMORY'].update({k: [
            {
                'question': q, 'answer': a, 'instruction': i, 'time_limit': t
            } for q, a, i, t in [
                ('Memorize this pattern:\nA5 → B8 → C3 → D7 → E2',
                 ['a5b8c3d7e2', 'A5B8C3D7E2'],
                 'Type the letters and numbers in sequence', 45),
                ('Remember these items:\nPHONE → KEY → BOOK → STAR → CLOCK',
                 ['phone key book star clock', 'PHONE KEY BOOK STAR CLOCK'],
                 'Type each item in order', 45)
            ]
        ] for k in ['medium']})
        self.exercises['MEMORY'].update({k: [
            {
                'question': q, 'answer': a, 'instruction': i, 'time_limit': t
            } for q, a, i, t in [
                ('Memorize this complex sequence:\nP7#K2@M9$R4*T6',
                 ['p7#k2@m9$r4*t6', 'P7#K2@M9$R4*T6'],
                 'Type the exact sequence including symbols', 60),
                ('Remember this pattern:\nRED TRIANGLE → BLUE CIRCLE → YELLOW SQUARE → WHITE DIAMOND',
                 ['red triangle blue circle yellow square white diamond',
                  'RED TRIANGLE BLUE CIRCLE YELLOW SQUARE WHITE DIAMOND'],
                 'Type the colors and shapes in order', 60)
            ]
        ] for k in ['hard']})
        
        self.exercises['LOGIC'] = {k: [
            {
                'question': q, 'answer': a, 'instruction': i, 'time_limit': t
            } for q, a, i, t in ex_data
        ] for k, ex_data in {
            'easy': [
                ('What continues this pattern?\n2 → 4 → 8 → 16 → ??\nEach number is related to the previous one.',
                 ['32', '32'], 'Find the next number that follows the pattern', 20),
                ('Solve this code:\nIf CAT = 24, DOG = 26, then PET = ??\nUse letter positions in alphabet.',
                 ['37', '37'], 'Calculate using letter positions', 20)
            ],
            'medium': [
                ('Complete the sequence:\n3 → 7 → 13 → 21 → ??\nThe increase between numbers follows a pattern.',
                 ['31', '31'], 'Find the pattern of increase', 30),
                ('Decode this pattern:\nSUN = 54, MOON = 56, STARS = ??\nConsider letter positions.',
                 ['77', '77'], 'Use letter positions and pattern', 30)
            ],
            'hard': [
                ('Solve this sequence:\n4 → 9 → 16 → 25 → 36 → ??\nThink about perfect squares.',
                 ['49', '49'], 'Find the mathematical relationship', 45),
                ('If TRIANGLE = 108, SQUARE = 81, then CIRCLE = ??\nConsider geometric properties.',
                 ['72', '72'], 'Use shape properties to solve', 45)
            ]
        }.items()}
        
        self.exercises['FOCUS'] = {k: [
            {
                'question': q, 'answer': a, 'instruction': i, 'time_limit': t
            } for q, a, i, t in ex_data
        ] for k, ex_data in {
            'easy': [
                ('Count in this text:\n"Mississippi River flows smoothly"\nHow many "s" letters appear?',
                 ['6', '6'], 'Count every occurrence of "s"', 20),
                ('In this text:\n"The quick brown fox jumps"\nHow many vowels (a,e,i,o,u) appear?',
                 ['5', '5'], 'Count all vowels', 20)
            ],
            'medium': [
                ('Find in this text:\n"she sells seashells by the seashore"\nHow many words contain "se"?',
                 ['4', '4'], 'Count words containing "se"', 30),
                ('Analyze this sentence:\n"Peter Piper picked pickled peppers"\nHow many words start with "p"?',
                 ['5', '5'], 'Count words starting with p', 30)
            ],
            'hard': [
                ('In this paragraph:\n"The theater thursday theme thought thoroughly through thirty themes"\nCount words with "th".',
                 ['7', '7'], 'Count words containing "th"', 45),
                ('Find in this text:\n"Apple arranges amazing arrays around arcade areas"\nCount words with double "a".',
                 ['4', '4'], 'Count words with two "a" letters', 45)
            ]
        }.items()}
        
        self.exercises['SPEED'] = {k: [
            {
                'question': q, 'answer': a, 'instruction': i, 'time_limit': t
            } for q, a, i, t in ex_data
        ] for k, ex_data in {
            'easy': [
                ('Type this sequence as fast as possible:\n1234567890',
                 ['1234567890'], 'Type all numbers in order', 15),
                ('Speed type these words:\ncat dog bird fish',
                 ['cat dog bird fish', 'CAT DOG BIRD FISH'], 'Type the words in order', 15)
            ],
            'medium': [
                ('Type this phrase:\nShe sells sea shells',
                 ['she sells sea shells', 'SHE SELLS SEA SHELLS'], 'Type exactly as shown', 20),
                ('Type in reverse:\nHappy Days 2024',
                 ['4202 syad yppah', '4202 SYAD YPPAH'], 'Type the text backwards', 25)
            ],
            'hard': [
                ('Type with precision:\nFive experts juggle quickly',
                 ['five experts juggle quickly', 'FIVE EXPERTS JUGGLE QUICKLY'], 'Type the sentence exactly', 20),
                ('Type with alternating case:\ncoding is fun',
                 ['CoDiNg Is FuN', 'cOdInG iS fUn'], 'Alternate between upper and lower case', 30)
            ]
        }.items()}
        
        self.difficulties = ['easy', 'medium', 'hard']

    def get_exercise(self, category, difficulty=None):
        # Selects a random exercise from specified category and difficulty
        if not difficulty:
            difficulty = random.choice(self.difficulties)
        return {**random.choice(self.exercises.get(category, {}).get(difficulty, [])), 'category': category, 'difficulty': difficulty} if category in self.exercises and difficulty in self.exercises[category] else None

    def check_answer(self, exercise, user_answer):
            # Checks user answer against all possible correct answers
        return user_answer.lower() in [ans.lower() for ans in exercise['answer']] if isinstance(exercise['answer'], list) else user_answer.lower() == exercise['answer'].lower()

    def calculate_score(self, is_correct, completion_time, time_limit):
        # Calculates score based on correctness and completion time
        # Base score: 100 points
        # Time bonus: up to 50 points based on completion speed
        # Maximum possible score: 150 points
        return min(150, 100 + (50 * max(0, (time_limit - completion_time) / time_limit))) if is_correct else 0

    def get_feedback(self, score):
        return next(fb for sc, fb in [(140, "OUTSTANDING! 🌟"), (120, "EXCELLENT! 🌟"), 
                                    (100, "GREAT WORK! 💫"), (80, "GOOD JOB! 👍"), 
                                    (0, "NICE TRY! 👍")] if score >= sc)