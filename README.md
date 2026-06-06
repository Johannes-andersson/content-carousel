# Carousel Generator

Generate punchy 6-slide carousel copy for TikTok, YouTube, and Facebook — powered by Claude.

## Slide structure

| Slide | Type | Limit |
|-------|------|-------|
| 1 | Hook | Max 12 words |
| 2–5 | Headline + Body | Headline max 6 words, Body max 20 words |
| 6 | CTA | Max 15 words, ends with "Follow for daily AI tips." |

Output is plain text — no markdown, no asterisks. Copy-paste ready.

---

## Setup

### 1. Clone or download this folder

Put `carousel-generator/` wherever you keep your projects.

### 2. Create a virtual environment

```bash
cd carousel-generator
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in (or create a free account)
3. Click **API Keys** in the left sidebar
4. Click **Create Key**, give it a name, copy the key

### 5. Add your key to a .env file

```bash
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your actual key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

The key is loaded at runtime — it is never hardcoded in the script.

---

## Run it

```bash
python carousel.py
```

You'll be prompted to enter a topic. The carousel prints to the terminal and is saved to `carousel_log.txt`.

---

## Tips for writing good topics

The more specific your topic, the better the output.

| Too vague | Better |
|-----------|--------|
| "AI tips" | "5 Claude prompts that save you 2 hours a day" |
| "Productivity" | "How solopreneurs use AI to replace a $5k/month assistant" |
| "ChatGPT" | "3 ChatGPT habits that separate beginners from power users" |

Good topic formats:
- **Number + outcome**: "7 ways AI can write your email newsletter in 10 minutes"
- **Mistake format**: "Why most people use AI wrong (and what to do instead)"
- **Before/after**: "What my workflow looked like before vs after AI tools"
- **Niche specific**: "How a freelance designer uses Claude to win more clients"

---

## Files

| File | Purpose |
|------|---------|
| `carousel.py` | Main script |
| `requirements.txt` | Python dependencies |
| `.env` | Your API key (you create this — not committed to git) |
| `.env.example` | Template for the .env file |
| `carousel_log.txt` | Auto-generated history of all carousels you've made |

---

## Model

Uses `claude-sonnet-4-6` — the current recommended Claude Sonnet model. Fast, cost-effective, and excellent at structured creative copy.

> **Note:** If you previously used `claude-sonnet-4-20250514`, that's a deprecated snapshot ID. The model string in `carousel.py` is already set to the correct current ID.

---

## Customisation

Open `carousel.py` to tweak:

- **`SYSTEM_PROMPT`** — change the tone, niche, or slide structure
- **`MAX_RETRIES`** — how many times to retry if the output isn't exactly 6 slides (default: 2)
- **`LOG_FILE`** — change the output log filename
- **`MODEL`** — swap to a different Claude model if needed
