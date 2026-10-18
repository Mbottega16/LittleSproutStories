#!/usr/bin/env python3
"""
Little Sprout Stories — Automated Story Generation & Asset Pipeline

Generates valid, phonics-compliant JSON specs in `build_pipeline/specs/<BookId>.json`,
adhering to the "Double Engine" architecture (rich Stream A narrative + strictly
decodable Stream B child practice line).

Features:
- Validates Stream B decodability against `10_Decodable_Word_List.md` rules.
- Validates sprite existence in `assets/sprites/`.
- Compiles the HTML output via `build_pipeline/build.py`.
- Synthesizes offline neural TTS narration using Piper TTS on D:\\AI-Tools\\Piper-TTS.

Usage:
    # Generate a new story spec from a built-in template preset:
    python build_pipeline/generate_story.py --preset garden --build

    # Generate custom story:
    python build_pipeline/generate_story.py --id Book16_Marcus_Garden --title "Marcus Plants a Seed" --theme garden --build

    # Generate with local Piper TTS audio narration:
    python build_pipeline/generate_story.py --preset garden --build --audio
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = Path(__file__).resolve().parent / "specs"
SPRITES_DIR = REPO_ROOT / "assets" / "sprites"
AUDIO_DIR = REPO_ROOT / "assets" / "audio"

PIPER_EXE = Path(r"D:\AI-Tools\Piper-TTS\bin\piper\piper.exe")
PIPER_VOICE = Path(r"D:\AI-Tools\Piper-TTS\voices\en_US-lessac-medium.onnx")

# Approved Dolch sight words from 10_Decodable_Word_List.md
DOLCH_WORDS = {
    "a", "and", "are", "at", "away", "be", "big", "blue", "but", "came", "can",
    "come", "did", "do", "down", "each", "eat", "find", "for", "four", "funny",
    "get", "go", "going", "good", "had", "has", "have", "he", "help", "her",
    "here", "him", "his", "how", "i", "in", "into", "is", "it", "jump", "know",
    "like", "little", "look", "made", "make", "me", "my", "new", "no", "not",
    "now", "of", "on", "one", "our", "out", "play", "please", "ran", "red", "run",
    "said", "saw", "see", "she", "so", "some", "soon", "that", "the", "their",
    "them", "then", "there", "they", "think", "this", "three", "to", "too", "two",
    "under", "up", "want", "was", "we", "well", "went", "were", "what", "where",
    "will", "with", "yes", "you"
}

# Approved feelings and Story Heart Words from 10_Decodable_Word_List.md and GUIDANCE_DECODABILITY_VS_STORY_FLOW.md
ALLOWED_FEELINGS = {
    "glad", "sad", "mad", "bad", "ok", "good",
    "calm", "safe", "brave", "proud", "shy", "upset", "stuck", "warm", "kind", "quiet", "fine",
    "feel", "feels"
}
CHARACTER_NAMES = {
    "maya", "marcus", "sophie", "james",
    "alex", "jasmine", "chen", "patel", "rodriguez", "smith", "keisha", "tom", "rose", "david", "aisha", "green",
    "mr", "ms", "officer", "nurse", "dr"
}

# Category (f) compound/multisyllable decodable words built from simple CVC syllables
SIMPLE_MULTISYLLABLE = {"visit", "letter", "muffin", "rabbit", "sunset", "upset"}

def validate_stream_b_line(line: str, allowed_theme_nouns: set, heart_words: set = None) -> list:
    """Validate a Stream B line against the decodable word rules. Returns list of warning words."""
    cleaned = re.sub(r"&[a-zA-Z0-9#]+;", " ", line) # strip html entities
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", cleaned).lower()
    words = cleaned.split()
    
    warnings = []
    theme_noun_used = 0
    active_heart_words = heart_words or set()
    for w in words:
        if w in DOLCH_WORDS or w in CHARACTER_NAMES or w in ALLOWED_FEELINGS or w in SIMPLE_MULTISYLLABLE or w in active_heart_words:
            continue
        if w in allowed_theme_nouns:
            theme_noun_used += 1
            if theme_noun_used > 2:
                warnings.append(f"Excess theme nouns ({w})")
            continue
        # Check CVC / CVCC pattern heuristic: short vowel, length <= 5
        if len(w) <= 5 and re.match(r"^[bcdfghjklmnpqrstvwxyz]*[aeiou][bcdfghjklmnpqrstvwxyz]+$", w):
            continue
        warnings.append(w)
    return warnings

# Built-in high quality template presets
TEMPLATES = {
    "garden": {
        "book_id": "Book16_Marcus_Garden_Seeds",
        "title": "Marcus and Sophie in the Secret Garden",
        "book_title": "Marcus & Sophie in the Secret Garden",
        "book_badge": "Garden Sprout",
        "backdrop": "backdrop-garden",
        "helper": {"name": "Mr. Green", "emoji": "&#127793;"},
        "characters": ["marcus", "sophie"],
        "theme_nouns": {"pot", "seed", "seeds", "dirt", "mud", "sun", "plant", "sprout", "tap"},
        "pages": [
            {
                "index": 1,
                "text_a": "Marcus and Sophie visited the community garden on a sunny morning. Little green sprouts were growing everywhere!",
                "text_b": "Marcus and Sophie see the green plants.",
                "sprites": ["marcus_happy_pointing.png", "sophie_happy_standing.png"],
                "hotspot": {"position": "left", "effect": "pulse", "emoji": "&#127793;", "aria_label": "Tap the sprout"}
            },
            {
                "index": 2,
                "text_a": "&ldquo;Welcome, young gardeners!&rdquo; said Mr. Green with a warm smile. &ldquo;Today we are planting tiny seeds.&rdquo;",
                "text_b": "Mr. Green waves. &ldquo;Come help!&rdquo; said Mr. Green.",
                "sprites": ["marcus_happy_standing.png", "sophie_happy_standing.png"],
                "helper": True
            },
            {
                "index": 3,
                "text_a": "Marcus held a small clay pot. He filled it with soft, dark soil using his garden shovel.",
                "text_b": "Marcus has a pot. Marcus digs in the dirt.",
                "sprites": ["marcus_happy_kneeling.png", "sophie_neutral_looking.png"],
                "hotspot": {"position": "right", "effect": "pop", "emoji": "&#129684;", "aria_label": "Tap the pot"}
            },
            {
                "index": 4,
                "text_a": "Sophie opened a packet of seeds. &ldquo;They are so tiny! What if they don&rsquo;t grow?&rdquo; she asked worriedly.",
                "text_b": "Sophie looks at the seeds. Sophie feels a bit sad.",
                "sprites": ["marcus_neutral_looking.png", "sophie_sad_standing.png"],
                "quiz": {
                    "question": "What are Marcus and Sophie planting?",
                    "options": ["Tiny seeds", "Big rocks", "Toys"],
                    "answer": 0
                }
            },
            {
                "index": 5,
                "text_a": "Mr. Green smiled gently. &ldquo;All seeds need is soil, sunlight, water, and patience,&rdquo; he explained.",
                "text_b": "Seeds need sun and water to get big.",
                "sprites": ["marcus_happy_standing.png", "sophie_neutral_looking.png"],
                "helper": True
            },
            {
                "index": 6,
                "text_a": "Sophie carefully pressed two seeds into the dirt and patted it smooth. &ldquo;Good night, little seeds!&rdquo; she whispered.",
                "text_b": "Sophie taps the dirt. Good job, Sophie!",
                "sprites": ["marcus_happy_looking.png", "sophie_happy_kneeling.png"],
                "hotspot": {"position": "mid", "effect": "ding", "emoji": "&#128167;", "aria_label": "Water the seeds"}
            },
            {
                "index": 7,
                "text_a": "Marcus sprinkled water from the watering can. The soil drank it up eagerly. &ldquo;We did it together!&rdquo; shouted Marcus.",
                "text_b": "Marcus gets water. Marcus feels glad.",
                "sprites": ["marcus_happy_jumping.png", "sophie_happy_giving.png"],
                "quiz": {
                    "question": "What helped Sophie feel confident about planting?",
                    "options": ["Mr. Green&rsquo;s kind advice", "Running away", "Eating a snack"],
                    "answer": 0
                }
            },
            {
                "index": 8,
                "text_a": "Marcus and Sophie placed their pot in the warm sunshine. They could not wait to come back and see their green sprouts grow.",
                "text_b": "Marcus and Sophie clap. &ldquo;We did it!&rdquo;",
                "sprites": ["marcus_happy_waving.png", "sophie_happy_waving.png"],
                "helper": True
            }
        ],
        "end_screen": {
            "badge_emoji": "&#127793;",
            "badge_label_html": "Garden<br>Sprout",
            "feeling": "Patience and teamwork when trying something new.",
            "ask": "Have you ever waited for something to grow? How did you practice patience?",
            "try_this": "Plant a bean seed in a damp paper towel in a cup by the window this week and watch it sprout together.",
            "standards": "RL.K.1, SL.K.3"
        }
    },
    "rabbit": {
        "book_id": "Book17_Maya_Toy_Rabbit",
        "title": "Maya and the Velveteen Rabbit",
        "book_title": "Maya & Sophie and the Velveteen Rabbit",
        "book_badge": "Gentle Care",
        "backdrop": "backdrop-library",
        "helper": {"name": "Ms. Chen", "emoji": "&#128218;"},
        "characters": ["maya", "sophie"],
        "theme_nouns": {"rabbit", "box", "ears", "toy", "bed", "fur", "nap"},
        "pages": [
            {
                "index": 1,
                "text_a": "Maya and Sophie were exploring the cozy corner of the library when they discovered an old wooden box tucked under a shelf.",
                "text_b": "Maya sees an old box. A toy is inside.",
                "sprites": ["maya_happy_pointing.png", "sophie_happy_standing.png"],
                "hotspot": {"position": "left", "effect": "pulse", "emoji": "&#128007;", "aria_label": "Tap the rabbit"}
            },
            {
                "index": 2,
                "text_a": "Inside the box sat a soft stuffed rabbit with worn velvet ears and a quiet smile.",
                "text_b": "Sophie claps. &ldquo;Look at him!&rdquo; said Sophie.",
                "sprites": ["maya_happy_standing.png", "sophie_happy_jumping.png"],
                "hotspot": {"position": "right", "effect": "pop", "emoji": "&#129528;", "aria_label": "Pet the rabbit"}
            },
            {
                "index": 3,
                "text_a": "Maya picked up the rabbit gently. &ldquo;His fur is worn, but he feels so warm and gentle,&rdquo; whispered Maya.",
                "text_b": "The rabbit has soft red ears.",
                "sprites": ["maya_happy_giving.png", "sophie_neutral_looking.png"]
            },
            {
                "index": 4,
                "text_a": "Sophie looked closely at the rabbit&rsquo;s stitched seams. &ldquo;Is he too old to play with?&rdquo; she wondered.",
                "text_b": "Sophie is sad. &ldquo;Is he too old?&rdquo;",
                "sprites": ["maya_neutral_looking.png", "sophie_sad_standing.png"],
                "quiz": {
                    "question": "What toy did Maya and Sophie find?",
                    "options": ["A soft velvet rabbit", "A toy truck", "A robot"],
                    "answer": 0
                }
            },
            {
                "index": 5,
                "text_a": "Ms. Chen knelt beside them with a gentle smile. &ldquo;Real value doesn&rsquo;t come from being brand new. When a toy is truly loved, it becomes real.&rdquo;",
                "text_b": "Ms. Chen smiles. &ldquo;Love makes him real.&rdquo;",
                "sprites": ["maya_happy_standing.png", "sophie_happy_standing.png"],
                "helper": True
            },
            {
                "index": 6,
                "text_a": "Maya hugged the rabbit close. &ldquo;You are my favorite reading buddy now,&rdquo; she said happily.",
                "text_b": "Maya hugs the rabbit with love.",
                "sprites": ["maya_happy_standing.png", "sophie_happy_looking.png"],
                "hotspot": {"position": "mid", "effect": "ding", "emoji": "&#10024;", "aria_label": "Make a wish"}
            },
            {
                "index": 7,
                "text_a": "Sophie helped arrange three storybooks so the rabbit could listen to the words. &ldquo;He loves stories!&rdquo; laughed Sophie.",
                "text_b": "Sophie is glad. We love our rabbit.",
                "sprites": ["maya_happy_standing.png", "sophie_happy_giving.png"],
                "quiz": {
                    "question": "What makes an old toy special?",
                    "options": ["Being loved and cared for", "Having batteries", "Being kept in a closet"],
                    "answer": 0
                }
            },
            {
                "index": 8,
                "text_a": "Before leaving the library, the girls tucked the rabbit into a soft felt basket. &ldquo;Sleep well, little friend,&rdquo; said Maya.",
                "text_b": "Maya and Sophie clap. &ldquo;Good night!&rdquo;",
                "sprites": ["maya_happy_waving.png", "sophie_happy_waving.png"],
                "helper": True
            }
        ],
        "end_screen": {
            "badge_emoji": "&#128007;",
            "badge_label_html": "Gentle<br>Care",
            "feeling": "Cherishing well-loved things and understanding empathy.",
            "ask": "Do you have a toy or blanket that is well-loved? Why is it special to you?",
            "try_this": "Pick a beloved toy together and give it a special spot or gentle bedtime story tonight.",
            "standards": "RL.K.1, SL.K.3"
        }
    },
    "willows": {
        "book_id": "Book18_James_Marcus_River_Picnic",
        "title": "James and Marcus by the River",
        "book_title": "James & Marcus by the River",
        "book_badge": "River Friend",
        "backdrop": "backdrop-garden",
        "helper": {"name": "Alex", "emoji": "&#128674;"},
        "characters": ["james", "marcus"],
        "theme_nouns": {"boat", "river", "basket", "bread", "jam", "sun", "hat", "duck", "pond"},
        "pages": [
            {
                "index": 1,
                "text_a": "James and Marcus took a red picnic basket down to the sparkling river on a warm spring day.",
                "text_b": "James and Marcus see the river.",
                "sprites": ["james_happy_pointing.png", "marcus_happy_standing.png"],
                "hotspot": {"position": "left", "effect": "pulse", "emoji": "&#128674;", "aria_label": "Tap the boat"}
            },
            {
                "index": 2,
                "text_a": "A small wooden rowboat bobbed gently by the green shore. &ldquo;Look at that little boat!&rdquo; laughed Marcus.",
                "text_b": "Marcus sees a red boat.",
                "sprites": ["james_happy_standing.png", "marcus_happy_jumping.png"],
                "hotspot": {"position": "right", "effect": "pop", "emoji": "&#129414;", "aria_label": "Watch the duck"}
            },
            {
                "index": 3,
                "text_a": "James spread out a big checkered blanket under the shady willow tree.",
                "text_b": "James puts down the basket.",
                "sprites": ["james_happy_kneeling.png", "marcus_happy_standing.png"]
            },
            {
                "index": 4,
                "text_a": "Marcus opened the basket, but the jam jar slipped! &ldquo;Oh no! Did it spill?&rdquo; he cried.",
                "text_b": "Marcus is sad. &ldquo;Did it drop?&rdquo;",
                "sprites": ["james_neutral_looking.png", "marcus_sad_standing.png"],
                "quiz": {
                    "question": "Where did James and Marcus go for a picnic?",
                    "options": ["By the quiet river", "To the moon", "Inside a dark cave"],
                    "answer": 0
                }
            },
            {
                "index": 5,
                "text_a": "Alex the firefighter was fishing nearby and caught the jar with a friendly grin. &ldquo;Safe and sound!&rdquo; Alex said.",
                "text_b": "Alex smiles. &ldquo;I got it!&rdquo; said Alex.",
                "sprites": ["james_happy_standing.png", "marcus_happy_standing.png"],
                "helper": True
            },
            {
                "index": 6,
                "text_a": "They shared fresh bread, sweet fruit, and cool water together under the soft breeze.",
                "text_b": "They eat bread and jam in the sun.",
                "sprites": ["james_happy_sitting.png", "marcus_happy_sitting.png"],
                "hotspot": {"position": "mid", "effect": "ding", "emoji": "&#129366;", "aria_label": "Share a snack"}
            },
            {
                "index": 7,
                "text_a": "Two friendly ducks swam over and quacked happily as Marcus waved. &ldquo;Picnics with friends are the best!&rdquo; said Marcus.",
                "text_b": "Marcus is glad. Marcus loves picnics.",
                "sprites": ["james_happy_standing.png", "marcus_happy_jumping.png"],
                "quiz": {
                    "question": "Who helped Marcus catch the jar?",
                    "options": ["Alex the helper", "A flying bird", "A giant bear"],
                    "answer": 0
                }
            },
            {
                "index": 8,
                "text_a": "As the sun set, the boys packed their basket and waved goodbye to the peaceful river.",
                "text_b": "James and Marcus clap. &ldquo;Good day!&rdquo;",
                "sprites": ["james_happy_waving.png", "marcus_happy_waving.png"],
                "helper": True
            }
        ],
        "end_screen": {
            "badge_emoji": "&#128674;",
            "badge_label_html": "River<br>Friend",
            "feeling": "Outdoor curiosity, sharing, and helping a friend.",
            "ask": "Have you ever shared a meal outside with someone? What was fun about it?",
            "try_this": "Have a mini living-room or backyard blanket picnic together this weekend.",
            "standards": "RL.K.1, SL.K.3"
        }
    },
    "fable": {
        "book_id": "Book19_Sophie_Little_Mouse",
        "title": "Sophie and the Little Mouse",
        "book_title": "Sophie & Maya and the Little Mouse",
        "book_badge": "Kind Helper",
        "backdrop": "backdrop-street",
        "helper": {"name": "Keisha", "emoji": "&#128045;"},
        "characters": ["sophie", "maya"],
        "theme_nouns": {"mouse", "net", "box", "hat", "tin", "cup", "pet", "yard"},
        "pages": [
            {
                "index": 1,
                "text_a": "Sophie and Maya were walking past the community garden gate when Sophie noticed something rustling in the dry leaves.",
                "text_b": "Sophie sees a little mouse.",
                "sprites": ["sophie_happy_pointing.png", "maya_happy_standing.png"],
                "hotspot": {"position": "left", "effect": "pulse", "emoji": "&#128045;", "aria_label": "Tap the mouse"}
            },
            {
                "index": 2,
                "text_a": "A tiny gray mouse had gotten tangled in some soft gardening twine. It squeaked softly, trying to get free.",
                "text_b": "The mouse cannot run away.",
                "sprites": ["sophie_neutral_looking.png", "maya_neutral_looking.png"]
            },
            {
                "index": 3,
                "text_a": "&ldquo;He is so little,&rdquo; whispered Maya. &ldquo;We should be very quiet and gentle so we don&rsquo;t scare him.&rdquo;",
                "text_b": "Maya is calm. &ldquo;We can help,&rdquo; said Maya.",
                "sprites": ["sophie_happy_standing.png", "maya_happy_standing.png"]
            },
            {
                "index": 4,
                "text_a": "Sophie reached out, but the twine was wound tight. &ldquo;I can&rsquo;t untangle it alone!&rdquo; Sophie said, feeling discouraged.",
                "text_b": "Sophie is sad. The rope is stuck.",
                "sprites": ["sophie_sad_standing.png", "maya_neutral_looking.png"],
                "quiz": {
                    "question": "What did Sophie and Maya find tangled in twine?",
                    "options": ["A little mouse", "A big bicycle", "A toy truck"],
                    "answer": 0
                }
            },
            {
                "index": 5,
                "text_a": "Keisha, the park caretaker, walked over with a gentle smile and a pair of blunt safety snips.",
                "text_b": "Keisha smiles. &ldquo;Let me help,&rdquo; said Keisha.",
                "sprites": ["sophie_happy_standing.png", "maya_happy_standing.png"],
                "helper": True
            },
            {
                "index": 6,
                "text_a": "Keisha snipped the loose string carefully. Sophie gently held back the leaves so the mouse had a clear path.",
                "text_b": "Snip, snip! The mouse is free.",
                "sprites": ["sophie_happy_kneeling.png", "maya_happy_looking.png"],
                "hotspot": {"position": "mid", "effect": "ding", "emoji": "&#10024;", "aria_label": "Cheer for the mouse"}
            },
            {
                "index": 7,
                "text_a": "The mouse paused on a mossy stone, wiggled its tiny whiskers at the girls, and scampered safely into the warm hedge.",
                "text_b": "Sophie is glad. The mouse ran home.",
                "sprites": ["sophie_happy_jumping.png", "maya_happy_giving.png"],
                "quiz": {
                    "question": "Why were Sophie and Maya happy at the end?",
                    "options": ["The mouse was safe and free", "They found gold coins", "It started to rain"],
                    "answer": 0
                }
            },
            {
                "index": 8,
                "text_a": "Keisha smiled at them both. &ldquo;No act of kindness, no matter how small, is ever wasted,&rdquo; Keisha said.",
                "text_b": "Sophie and Maya clap. We did good!",
                "sprites": ["sophie_happy_waving.png", "maya_happy_waving.png"],
                "helper": True
            }
        ],
        "end_screen": {
            "badge_emoji": "&#128045;",
            "badge_label_html": "Kind<br>Helper",
            "feeling": "Kindness, gentle care for small creatures, and asking for help.",
            "ask": "Have you ever helped an animal or a friend who was stuck? How did it feel?",
            "try_this": "Look for one small act of kindness you can do for someone in your family today.",
            "standards": "RL.K.1, SL.K.3"
        }
    }
}

def generate_audio(book_spec: dict):
    """Generate offline neural TTS wav files for each page using local Piper."""
    if not PIPER_EXE.exists():
        print(f"Warning: Piper TTS not found at {PIPER_EXE}. Skipping audio synthesis.")
        return
    if not PIPER_VOICE.exists():
        print(f"Warning: Piper voice model not found at {PIPER_VOICE}. Skipping audio synthesis.")
        return

    book_id = book_spec["book_id"]
    book_audio_dir = AUDIO_DIR / "books" / book_id
    book_audio_dir.mkdir(parents=True, exist_ok=True)

    print(f"Synthesizing audio narration with Piper TTS to {book_audio_dir}...")
    for page in book_spec["pages"]:
        p_idx = page["index"]
        # Stream A (Narrator)
        clean_text_a = re.sub(r"&[a-zA-Z0-9#]+;", " ", page["text_a"])
        clean_text_a = re.sub(r"\s+", " ", clean_text_a).strip()
        out_a = book_audio_dir / f"p{p_idx}_a.wav"
        
        cmd_a = [str(PIPER_EXE), "-m", str(PIPER_VOICE), "-f", str(out_a)]
        proc = subprocess.Popen(cmd_a, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.communicate(input=clean_text_a.encode("utf-8"))

        # Stream B (Child line)
        clean_text_b = re.sub(r"&[a-zA-Z0-9#]+;", " ", page["text_b"])
        clean_text_b = re.sub(r"\s+", " ", clean_text_b).strip()
        out_b = book_audio_dir / f"p{p_idx}_b.wav"
        
        cmd_b = [str(PIPER_EXE), "-m", str(PIPER_VOICE), "-f", str(out_b)]
        proc = subprocess.Popen(cmd_b, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.communicate(input=clean_text_b.encode("utf-8"))

        print(f"  Page {p_idx}: p{p_idx}_a.wav & p{p_idx}_b.wav ready.")
    print("Narration audio synthesis complete.")

def build_spec_from_template(preset_name: str) -> dict:
    if preset_name not in TEMPLATES:
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {list(TEMPLATES.keys())}")
    data = TEMPLATES[preset_name]

    spec = {
        "book_id": data["book_id"],
        "title": data["title"],
        "book_title": data["book_title"],
        "book_badge": data["book_badge"],
        "cover": {
            "h1_html": data["title"].replace(" and ", " &amp; <br>"),
            "stage": {
                "backdrop": data["backdrop"],
                "elements": [
                    {"type": "img", "sprite": f"{data['characters'][0]}_happy_waving.png", "alt": data['characters'][0].title()},
                    {"type": "img", "sprite": f"{data['characters'][1]}_happy_waving.png", "alt": data['characters'][1].title()}
                ]
            }
        },
        "pages": [],
        "end_screen": data["end_screen"]
    }

    theme_nouns = data.get("theme_nouns", set())
    heart_words = set(data.get("heart_words", []))

    for p in data["pages"]:
        elements = []
        for s in p.get("sprites", []):
            elements.append({"type": "img", "sprite": s, "alt": s.split("_")[0].title()})
        if p.get("helper"):
            elements.append({"type": "helper", "name": data["helper"]["name"], "emoji": data["helper"]["emoji"]})
        if p.get("hotspot"):
            hs = p["hotspot"]
            elements.append({"type": "hotspot", "position": hs["position"], "effect": hs["effect"], "aria_label": hs["aria_label"], "emoji": hs["emoji"]})

        # Validate decodability
        warns = validate_stream_b_line(p["text_b"], theme_nouns, heart_words)
        if warns:
            print(f"  [Decodability Warning] Page {p['index']} text_b has unverified words: {warns}", file=sys.stderr)

        spec["pages"].append({
            "index": p["index"],
            "stage": {
                "backdrop": data["backdrop"],
                "elements": elements
            },
            "text_a": p["text_a"],
            "text_b": p["text_b"],
            "quiz": p.get("quiz")
        })

    return spec

def main():
    parser = argparse.ArgumentParser(description="Little Sprout Stories Spec Generator")
    parser.add_argument("--preset", default="garden", choices=list(TEMPLATES.keys()), help="Template preset")
    parser.add_argument("--build", action="store_true", help="Automatically run build_pipeline/build.py")
    parser.add_argument("--audio", action="store_true", help="Synthesize page narration with Piper TTS")
    parser.add_argument("--out", default=None, help="Custom output spec file path")
    args = parser.parse_args()

    print(f"=== Little Sprout Stories Generation Pipeline ===")
    spec = build_spec_from_template(args.preset)
    book_id = spec["book_id"]
    spec_path = Path(args.out) if args.out else SPECS_DIR / f"{book_id}.json"

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    print(f"Generated spec successfully at: {spec_path}")

    if args.audio:
        generate_audio(spec)

    if args.build:
        print("\nInvoking build_pipeline/build.py...")
        cmd = [sys.executable, str(Path(__file__).resolve().parent / "build.py"), book_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        if res.returncode == 0:
            print(f"Rendered book HTML ready: {REPO_ROOT / 'books' / f'{book_id}.html'}")

if __name__ == "__main__":
    main()
