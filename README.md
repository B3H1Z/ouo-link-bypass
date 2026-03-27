# ouo-bypass
Script to bypass ouo.io/press short links (incl reCaptcha v3 bypass) and a Telegram bot interface for it.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Requires Python 3.10+.

Create/edit `.env` in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Run Telegram Bot

```bash
python3 main.py
```

If `TELEGRAM_BOT_TOKEN` is empty or missing, startup fails fast with a clear error.

## Run Direct Bypass (No Bot)

You can run `ouo_bypass.py` directly with one or more URLs:

```bash
python3 ouo_bypass.py https://ouo.io/on5by
python3 ouo_bypass.py https://ouo.io/on5by https://ouo.press/xxxx
```

## Pre-Publish Checklist

- Keep `.env` out of git and only commit `.env.example`.
- Ensure `.venv/`, `__pycache__/`, and `.DS_Store` are ignored.
- Verify direct mode: `python3 ouo_bypass.py <url>`.
- Verify bot mode: `python3 main.py` (with a valid token in `.env`).
