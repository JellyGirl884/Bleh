import random
import re
from typing import List, Tuple

# 20 Curse Types
CURSE_TYPES = [
    "no_vowels",
    "no_e",
    "reverse",
    "morse_code",
    "pig_latin",
    "shuffle",
    "stutter",
    "yoda_speak",
    "pirate_speak",
    "emoji_prefix",
    "robotic",
    "slowmo",
    "random_caps",
    "spelling_bee",
    "uwu_speak",
    "math_curse",
    "upside_down",
    "doubletalk",
    "binary_prefix",
    "backwards_words"
]

MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' / '
}

UPSIDE_DOWN_DICT = {
    'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ',
    'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u',
    'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n',
    'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 'y': 'ʎ', 'z': 'z'
}

def apply_curse(text: str, curse_type: str) -> str:
    """Apply a curse effect to text"""
    
    if curse_type == "no_vowels":
        return re.sub(r'[aeiouAEIOU]', '', text)
    
    elif curse_type == "no_e":
        return text.replace('e', '').replace('E', '')
    
    elif curse_type == "reverse":
        return text[::-1]
    
    elif curse_type == "morse_code":
        return ' '.join(MORSE_CODE_DICT.get(char.lower(), char) for char in text)
    
    elif curse_type == "pig_latin":
        words = text.split()
        pig_words = []
        for word in words:
            if len(word) > 0 and word[0].lower() in 'aeiou':
                pig_words.append(word + 'way')
            elif len(word) > 0:
                pig_words.append(word[1:] + word[0].lower() + 'ay')
        return ' '.join(pig_words)
    
    elif curse_type == "shuffle":
        words = text.split()
        shuffled = []
        for word in words:
            if len(word) > 3:
                middle = list(word[1:-1])
                random.shuffle(middle)
                shuffled.append(word[0] + ''.join(middle) + word[-1])
            else:
                shuffled.append(word)
        return ' '.join(shuffled)
    
    elif curse_type == "stutter":
        return ''.join(char * 2 if char.isalpha() else char for char in text)
    
    elif curse_type == "yoda_speak":
        words = text.split()
        return ' '.join(reversed(words))
    
    elif curse_type == "pirate_speak":
        replacements = {
            'hello': 'ahoy',
            'friend': 'matey',
            'yes': 'aye',
            'no': 'nay',
            'you': 'ye',
            'the': 'th'
        }
        result = text.lower()
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result + " Yarr!"
    
    elif curse_type == "emoji_prefix":
        emojis = ['🔥', '💀', '⚡', '🎭', '🌙', '👻', '🎪', '🎨']
        return f"{random.choice(emojis)} {text}"
    
    elif curse_type == "robotic":
        return text.upper() + " [BEEP BOOP]"
    
    elif curse_type == "slowmo":
        return ' '.join(list(text))
    
    elif curse_type == "random_caps":
        return ''.join(char.upper() if random.choice([True, False]) else char.lower() for char in text)
    
    elif curse_type == "spelling_bee":
        return ' '.join(list(text))
    
    elif curse_type == "uwu_speak":
        text = text.replace('r', 'w').replace('l', 'w')
        text = text.replace('R', 'W').replace('L', 'W')
        return text + " uwu"
    
    elif curse_type == "upside_down":
        return ''.join(UPSIDE_DOWN_DICT.get(char.lower(), char) if char.isalpha() else char for char in reversed(text))
    
    elif curse_type == "doubletalk":
        words = text.split()
        return ' '.join(f"{word} {word[::-1]}" for word in words)
    
    elif curse_type == "binary_prefix":
        binary = bin(hash(text) & 0xffffffff)[2:]
        return f"[{binary}] {text}"
    
    elif curse_type == "backwards_words":
        words = text.split()
        return ' '.join(word[::-1] for word in words)
    
    else:
        return text

def generate_math_problem() -> Tuple[str, int]:
    """Generate a random math problem (addition or multiplication)
    Returns: (problem_string, answer)
    """
    problem_type = random.choice(['addition', 'multiplication'])
    
    if problem_type == 'addition':
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        answer = num1 + num2
        return f"{num1} + {num2} = ?", answer
    else:  # multiplication
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        answer = num1 * num2
        return f"{num1} × {num2} = ?", answer

def get_curse_description(curse_type: str) -> str:
    """Get a description of what a curse does"""
    descriptions = {
        "no_vowels": "All vowels are removed",
        "no_e": "The letter 'e' cannot be used",
        "reverse": "Messages are reversed",
        "morse_code": "Messages are converted to Morse code",
        "pig_latin": "Messages are converted to Pig Latin",
        "shuffle": "Words have their letters shuffled",
        "stutter": "Every letter is doubled",
        "yoda_speak": "Word order is reversed",
        "pirate_speak": "Speak like a pirate!",
        "emoji_prefix": "Random emoji added to messages",
        "robotic": "SHOUT LIKE A ROBOT",
        "slowmo": "Words are spelled out letter by letter",
        "random_caps": "Random letters are capitalized",
        "spelling_bee": "Every letter is separated",
        "uwu_speak": "R's and L's become W's",
        "math_curse": "Solve a math problem to send each message",
        "upside_down": "Text is reversed and flipped",
        "doubletalk": "Every word is doubled and reversed",
        "binary_prefix": "Messages have a binary prefix",
        "backwards_words": "Every word is spelled backwards"
    }
    return descriptions.get(curse_type, "Unknown curse")
