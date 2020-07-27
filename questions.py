# Envisage - Ryan Bradshaw
import pygame as pg

class Question():
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

question_prompts_easy = [
    "What is the equation for the area of a triangle?", "What is the equation for Pythagoras' Theorem?", "Where is the cerebrum located?", "Which king does Macbeth kill?",
    "Which planet is closest to the Sun?", "What's the biggest ocean?", "How many ghosts were there in Christmas Carol?", "Veins take blood to the heart.",
    "What is the biggest animal in the world?", "When was the battle of hastings?", "How many years did WWII last?", "When did the Titanic sink?",
    "The xylem transports food."
]

answer_prompts_easy = [
    ["1/2bh (a)", "2bhw (b)"], ["a^2 = b^2 + c^2 (a)", "a^2 + b^2 + c^2 = 1 (b)"], ["In the heart (a)", "In the brain (b)"], ["King Duncan (a)", "King Banquo (b)"],
    ["Jupiter (a)", "Mercury (b)"], ["Atlantic (a)", "Pacific (b)"], ["4 (a)", "3 (b)"], ["True (a)", "False (b)"], ["Blue whale (a)", "Elephant (b)"], ["1814 (a)", "1066 (b)"],
    ["6 years (a)", "4 years (b)"], ["1912 (a)", "1913 (b)"], ["True (a)", "False (b)"]
]

answers_easy = [
    pg.K_a, pg.K_a, pg.K_b, pg.K_a, pg.K_b, pg.K_b, pg.K_a, pg.K_a, pg.K_a, pg.K_b, pg.K_a, pg.K_a, pg.K_b
]

question_prompts_med = [
    "Which equation links F, W and d?", "What is the unit for Kinetic Energy?", "What is the value of g?", "Which equation is linked to Newton's Second Law?",
    "Principle of moments:", "When do SUVAT equations apply?", "Which equation links V, P, and I?", "What is the relative charge of an electron?",
    "What does the thumb represent in Flemming's Left Hand Rule?", "Which equation links m, E and v?"
]

answer_prompts_med = [
    ["W = Fd (a)", "d = F/W (b)"], ["J (a)", "Nm (b)"], ["6.21 (a)", "9.81 (b)"], ["F = ma (a)", "GPE = mgh (b)"],
    ["Moments always add to 100 (a)", "Total clockwise moment = Total anticlockwise moment (b)"], ["When acceleration is constant (a)", "When there is no gravity (b)"],
    ["P = IV (a)", "V = IP (b)"], ["0 (a)", "-1 (b)"],
    ["Magnetic Field (a)", "Force (b)"], ["E = 1/2mv^2 (a)", "m = Ev (b)"]
]

answers_med = [
    pg.K_a, pg.K_a, pg.K_b, pg.K_a, pg.K_b, pg.K_a, pg.K_a, pg.K_b, pg.K_b, pg.K_a
]
