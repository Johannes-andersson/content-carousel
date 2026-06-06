#!/Users/johan/Documents/Claude/Code-projects/carousel-generator/venv/bin/python
"""
carousel.py — Generate 6-slide carousel copy for TikTok/YouTube/Facebook.
Uses the Anthropic Claude API. API key is loaded from a .env file — never hardcoded.

Slide structure:
  Slide 1: HOOK          — max 12 words
  Slides 2-5: CONTENT    — headline max 6 words, body max 20 words
  Slide 6: CTA           — max 15 words, always ends with "Follow for daily AI tips."

Usage:
  python carousel.py
"""

import os
import re
import datetime
from pathlib import Path
from dotenv import load_dotenv
import anthropic

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

# Load the ANTHROPIC_API_KEY from your .env file
load_dotenv()

LOG_FILE = "carousel_log.txt"
MAX_RETRIES = 2  # How many times to retry if the output isn't exactly 6 slides

# The model to use. claude-sonnet-4-6 is the current recommended Sonnet model.
MODEL = "claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# PROMPT
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a social media copywriter for an AI/solopreneur brand.
Your audience loves practical AI tips, side hustles, and working smarter with AI tools.
Your tone is direct, punchy, and practical — no fluff, no hype, just value.

Write carousel copy in EXACTLY this format (6 slides, nothing else):

SLIDE 1 — HOOK
[One punchy sentence. Max 12 words. Make them stop scrolling.]

SLIDE 2 — HEADLINE
[Max 6 words]
BODY
[Max 20 words. One clear, actionable insight.]

SLIDE 3 — HEADLINE
[Max 6 words]
BODY
[Max 20 words. One clear, actionable insight.]

SLIDE 4 — HEADLINE
[Max 6 words]
BODY
[Max 20 words. One clear, actionable insight.]

SLIDE 5 — HEADLINE
[Max 5 words]
BODY
[Max 20 words. One clear, actionable insight.]

SLIDE 6 — CTA
[Max 15 words. End with exactly: Follow for daily AI tips.]

Rules:
- No markdown. No asterisks. No bullet points. No emojis.
- Plain text only — copy-paste ready.
- Stay under the word limits for every slide.
- Output exactly 6 slides, nothing more, nothing less.
- Do not include any intro text, explanations, or commentary outside the slides.
"""

def build_user_prompt(topic: str) -> str:
    return f"Write a 6-slide carousel about: {topic}"


# ---------------------------------------------------------------------------
# API CALL
# ---------------------------------------------------------------------------

def generate_carousel(client: anthropic.Anthropic, topic: str) -> str:
    """Call the Claude API and return the raw response text."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_user_prompt(topic)}
        ],
    )
    # Extract the text from the first content block
    return response.content[0].text


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

def count_slides(text: str) -> int:
    """Count how many SLIDE N markers appear in the output."""
    # Matches "SLIDE 1", "SLIDE 2", ... "SLIDE 6"
    matches = re.findall(r"SLIDE\s+\d+", text, re.IGNORECASE)
    return len(matches)


def is_valid(text: str) -> bool:
    """Return True if the output contains exactly 6 slides."""
    return count_slides(text) == 6


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def resolve_save_path() -> Path:
    """Open a native Mac folder picker via osascript. Falls back to current folder if dismissed."""
    import subprocess

    result = subprocess.run(
        ["osascript", "-e", 'POSIX path of (choose folder with prompt "Choose a folder to save your carousel:")'],
        capture_output=True,
        text=True,
    )

    folder = result.stdout.strip()

    if not folder:
        print("No folder chosen. Saving in current folder instead.")
        return Path.cwd() / LOG_FILE

    return Path(folder) / LOG_FILE


def append_to_log(topic: str, carousel_text: str) -> None:
    """Ask where to save, then append the carousel with date and topic."""
    save_path = resolve_save_path()

    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    divider = "=" * 60
    entry = f"\n{divider}\nDATE: {date_str}\nTOPIC: {topic}\n{divider}\n{carousel_text}\n"

    with open(save_path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"Saved to {save_path}")


# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

def print_carousel(text: str) -> None:
    """Print the carousel cleanly to the terminal."""
    print("\n" + "-" * 60)
    print(text.strip())
    print("-" * 60 + "\n")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # Check that the API key is available
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        return

    # Initialise the Anthropic client (picks up the key automatically from env)
    client = anthropic.Anthropic(api_key=api_key)

    print("\nCarousel Generator — powered by Claude")
    print("--------------------------------------")
    print("Type a topic and hit Enter. Press Ctrl+C or type 'q' to quit.\n")

    while True:
        topic = input("Enter your carousel topic: ").strip()

        if not topic or topic.lower() == "q":
            print("Bye!")
            break

        # Generate with retry loop
        carousel_text = None
        for attempt in range(1, MAX_RETRIES + 2):  # +2 so attempt 1 = first try
            if attempt > 1:
                print(f"Output didn't have exactly 6 slides. Retrying... (attempt {attempt})")

            carousel_text = generate_carousel(client, topic)

            if is_valid(carousel_text):
                break  # Good output — stop retrying
            elif attempt == MAX_RETRIES + 1:
                print(f"Warning: Could not get a clean 6-slide output after {MAX_RETRIES + 1} attempts.")
                print("Printing best result anyway.\n")

        # Print the result
        print_carousel(carousel_text)

        # Save to log
        append_to_log(topic, carousel_text)
        print()


if __name__ == "__main__":
    main()
