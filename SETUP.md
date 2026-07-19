# Spectandi SDK — Complete Setup Guide

This guide assumes **zero prior experience** with Python, terminals, or command lines. If you've never written code before, start here. If you're comfortable with Python already, the [Quickstart](https://github.com/volshenok/spectandi#quickstart) in the README is faster.

By the end of this guide, you'll have sent your first trace to your Spectandi dashboard and seen it appear.

**Estimated time:** about 20–30 minutes if this is your first time writing any code or using a terminal. If you already have Python installed, closer to 10 minutes.

**Stuck at any point?** Skip the rest of this guide and [book a 15-minute call](https://cal.com/spectandi/15min) — we'll walk through it together, live. No shame in that; this stuff trips up experienced developers too.

---

## What you'll need before starting

1. A Spectandi account — [sign up here](https://spectandi.com/signup) if you haven't already.
2. An Anthropic API key — see [Getting your Anthropic API key](#getting-your-anthropic-api-key) below if you don't have one.
3. About 10 minutes.

---

## Step 1: Install Python (skip if you already have it)

**Check if you already have Python installed.**

Open a terminal:

- **Windows:** Press the `Windows` key, type `PowerShell`, press Enter.
- **Mac:** Press `Cmd + Space`, type `Terminal`, press Enter.

Type this and press Enter:

```
python --version
```

- **If you see something like `Python 3.11.4`** — you have Python. Skip to Step 2.
- **If you see an error** (like "not recognized" or "command not found") — you need to install it first.

**Installing Python (Windows or Mac):**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button.
3. Run the installer.
4. **On Windows specifically: check the box that says "Add Python to PATH" before clicking Install.** This is the single most common thing people miss, and skipping it means the `python` command won't work afterward.
5. Once installed, close and reopen your terminal, then run `python --version` again to confirm it worked.

---

## Step 2: Get your Spectandi API key

1. Log into [spectandi.com](https://spectandi.com) and go to your dashboard.
2. If this is a new account, you'll see a **Quickstart** panel with a "Generate API key" button. Click it.
3. Your key will appear once, starting with `spct_live_...`. **Copy it now** using the copy button next to it.

> ⚠️ **This is the only time you'll ever see this key.** If you navigate away or refresh before copying it, you cannot get that exact key back — you'd need to generate a new one. There's no harm in generating a new one if that happens; the old one just won't work anymore.

Paste it somewhere temporary for now (a Notes app, a sticky note — anywhere you can copy it from again in a minute).

---

## Step 3: Getting your Anthropic API key

Spectandi traces calls to Claude (Anthropic's AI models), so you need your own Anthropic API key too — this is separate from your Spectandi key, and it's what lets your code actually talk to Claude.

1. Go to [console.anthropic.com](https://console.anthropic.com) and sign up or log in.
2. Go to **API Keys** in the left sidebar.
3. Click **Create Key**, give it any name (e.g. "spectandi-test").
4. Copy the key — it starts with `sk-ant-...`. Same rule as before: copy it now, you may not be able to see it again later.

> **Note:** Anthropic API usage costs a small amount of money per call (a fraction of a cent for a short test message like the one in this guide). You'll need a payment method on file with Anthropic to use their API. This is completely separate from Spectandi's own pricing.

---

## Step 4: Create your test file

This is the step where most mistakes happen, so follow it precisely.

**Do NOT use Notepad for this if you're on Windows.** Notepad has a habit of secretly saving files as `something.py.txt` instead of `something.py`, even though it looks correct — and that one hidden character difference will stop everything from working, with a confusing error. Use **VS Code** instead — it's free, and it's what most people writing Python actually use.

1. Download and install [VS Code](https://code.visualstudio.com/) if you don't have it.
2. Open VS Code.
3. Go to **File → New Text File** (or press `Ctrl+N` / `Cmd+N`).
4. Paste in this code exactly:

```python
import os
os.environ["SPECTANDI_API_KEY"] = "paste-your-spectandi-key-here"
os.environ["ANTHROPIC_API_KEY"] = "paste-your-anthropic-key-here"

from spectandi import tracked_chat

result = tracked_chat("Hello world", agent_name="my-first-agent")
print(result)
```

5. **Replace both placeholder strings** with your real keys from Steps 2 and 3 — keep the quotation marks around each key, just swap out the text inside them.

   A common mistake: forgetting the quotation marks entirely. Both of these lines need quotes around the key:
   ```python
   os.environ["SPECTANDI_API_KEY"] = "spct_live_abc123..."     ✅ correct
   os.environ["SPECTANDI_API_KEY"] = spct_live_abc123...       ❌ will cause an error
   ```

6. Save the file: **File → Save As**. Name it `quickstart_test.py` (make sure it really ends in `.py`, not `.py.txt`). Save it somewhere easy to find — your Desktop is fine.

---

## Step 5: Install the Spectandi package

Back in your terminal (PowerShell on Windows, Terminal on Mac), type this and press Enter:

```
pip install spectandi
```

You'll see some text scroll by as it downloads and installs. When it's done, you'll see your terminal prompt return, ready for the next command. If you see a "Successfully installed" message, that's a good sign.

**If you see an error** like "pip is not recognized" — this usually means Python didn't install correctly in Step 1. Go back and confirm `python --version` works before continuing.

---

## Step 6: Navigate to where you saved your file

You need to tell the terminal which folder your `quickstart_test.py` file is in.

**If you saved it to your Desktop**, type:

**Windows:**
```
cd $env:USERPROFILE\Desktop
```

**Mac:**
```
cd ~/Desktop
```

**To double-check the file is really there**, type:

**Windows:**
```
dir quickstart_test.py
```

**Mac:**
```
ls quickstart_test.py
```

If it lists the file, you're good. If it says "not found," the file saved somewhere else — check what folder VS Code's save dialog actually used, and `cd` there instead.

---

## Step 7: Run it

Type:

```
python quickstart_test.py
```

Press Enter.

**If it works**, you'll see Claude's actual reply printed in your terminal — something like:

```
Hello! How can I help you today?
```

**That's it — you just sent your first trace to Spectandi.**

---

## Step 8: Check your dashboard

Go back to [spectandi.com](https://spectandi.com) and refresh your dashboard. Within about a minute, your Quickstart panel should disappear and be replaced by your actual stats — showing the call you just made.

If it's been a couple of minutes and nothing's changed, that's fine — refresh the page manually once. Sometimes the very first trace takes a little longer to show up while the system "wakes up," especially if it's the first activity in a while.

---

## Troubleshooting common errors

**`NameError: name 'sk' is not defined` (or similar, mentioning `spct`)**
You forgot the quotation marks around one of your keys. Go back to Step 4 and make sure both key lines look like `"your-key-here"`, with quotes on both sides.

**`Could not resolve authentication method`**
Your `ANTHROPIC_API_KEY` line is missing, empty, or has a typo. Double check Step 4 — both key lines need to be there, both need real keys (not the placeholder text), and both need to come before the `from spectandi import tracked_chat` line.

**`No such file or directory`**
The terminal is looking in the wrong folder. Go back to Step 6 and confirm you've navigated (`cd`) to the folder where you actually saved `quickstart_test.py`.

**`'python' is not recognized...` / `command not found: python`**
Python isn't installed, or wasn't added to your system's PATH. Revisit Step 1 — on Windows, this almost always means the "Add Python to PATH" checkbox was missed during install; you may need to reinstall and check that box.

**The file runs but nothing happens / hangs for a long time**
This can happen if it's your very first request in a while and the underlying systems are "waking up" from being idle. Give it up to 30–60 seconds before assuming something's wrong.

**Something else entirely**
Copy the exact error message you're seeing and [book a 15-minute call](https://cal.com/spectandi/15min) — send it ahead of time if you can, or we'll debug it live together.

---

## What's next

Once your first trace is showing up, you can start replacing `"Hello world"` with real prompts from your own AI agent's code — anywhere your code currently calls Claude directly, wrap that call in `tracked_chat()` instead (or alongside it) to start capturing real telemetry.

Full technical reference, parameters, and source code: [github.com/volshenok/spectandi](https://github.com/volshenok/spectandi)

Questions, feedback, or something in this guide didn't work as described? Email [hello@spectandi.com](mailto:hello@spectandi.com) — we read every message, and if something here is unclear, that's useful information for us too.
