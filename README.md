## 🤖 Discord Bot - Leaderboard & Curses

A feature-rich Discord bot with a **points leaderboard system** and **20 unique curse types**!

### ✨ Features

#### 📊 Leaderboard System
- **`/leaderboard [limit]`** - View the top players (default: top 10)
- **`/give-points @member <points>`** - Add points to a member (Admin only)
- **`/remove-points @member <points>`** - Remove points from a member (Admin only)
- **`/reset-leaderboard`** - Reset all points to 0 (Admin only, requires confirmation)
- Persistent SQLite database for all leaderboard data

#### 🔥 Curse System (20 Unique Curses)
- **Text Effects**: no_vowels, no_e, reverse, morse_code, pig_latin, alternating_caps, random_caps, double_letter
- **Word Manipulation**: shuffle, stutter, yoda_speak, pirate_speak, slowmo, bubble_text, mirror
- **Special Effects**: uppercase, lowercase, robotic, emoji_prefix
- **Math Curse**: Users must solve addition/multiplication problems to send messages!

**Commands:**
- **`/curse @member <curse_type> <duration_hours>`** - Apply a curse (Admin only)
- **`/curses @member`** - View active curses on a user
- **`/lift-curse @member`** - Remove all curses from a user (Admin only)

### 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
   
   > ⚠️ **Never share your bot token!** If you accidentally expose it, regenerate it immediately in the Discord Developer Portal.

3. **Run the bot:**
   ```bash
   python main.py
   ```

### 📁 Project Structure

```
.
├── main.py              # Bot initialization and cog loader
├── database.py          # SQLite database manager
├── curses.py            # Curse types and effects
├── requirements.txt     # Python dependencies
├── .env                 # Discord token (add to .gitignore!)
├── .gitignore           # Git ignore rules
├── cogs/
│   ├── __init__.py
│   ├── leaderboard.py   # Leaderboard commands
│   └── curses.py        # Curse commands and effects
└── data/
    └── leaderboard.db   # SQLite database (auto-created)
```

### 🎮 Usage Examples

**Adding points:**
```
/give-points @JellyGirl884 50
```

**Viewing leaderboard:**
```
/leaderboard 20
```

**Applying a curse:**
```
/curse @Member no_e 6
```
(This user cannot use the letter 'e' for 6 hours!)

**Solving math curse:**
```
/curse @Member math_curse 3
```
User must type the answer to a math problem to send any message for 3 hours.

### 📝 Available Curse Types

| Curse | Effect |
|-------|--------|
| `no_vowels` | Remove all vowels from messages |
| `no_e` | Cannot use the letter 'e' |
| `reverse` | Reverse all messages |
| `morse_code` | Convert messages to morse code |
| `pig_latin` | Convert to Pig Latin |
| `uppercase` | Everything is UPPERCASE |
| `lowercase` | everything is lowercase |
| `shuffle` | Shuffle words in messages |
| `stutter` | S-s-stutter on every word |
| `yoda_speak` | Speak like Yoda you must |
| `pirate_speak` | Arr, talk like a pirate ye must |
| `alternating_caps` | AlTeRnAtE cApItAlS |
| `robotic` | [BEEP BOOP] Speak robotically |
| `emoji_prefix` | Add emoji before each word |
| `slowmo` | Add... delays... between... words |
| `random_caps` | RaNdOmLy MaKe SoMe CaPs |
| `bubble_text` | Put every word in bubbles |
| `mirror` | Flip horizontally (reversed mirror) |
| `math_curse` | Solve math problems to send messages |
| `double_letter` | Double every letter |

### ⚙️ Configuration

- **Database location:** `data/leaderboard.db` (auto-created on first run)
- **Math curse types:** Addition and Multiplication
- **Curse expiration:** Automatic when duration expires
- **Multiple curses:** Users can have multiple active curses simultaneously

### 🔒 Permissions

- **Leaderboard viewing:** Everyone
- **Admin commands:** Require Administrator permission in the server

### 📋 Requirements

- Python 3.9+
- discord.py 2.3.2
- python-dotenv

### 💡 Tips

- Use `/curses @member` to see remaining time on curses
- The math curse is the most challenging - use it wisely! 😄
- Curses automatically expire after the set duration
- Run `/reset-leaderboard` to start fresh (Admin only)

### 📞 Support

If you encounter issues:
1. Check that your bot has the required permissions (message management, embed links)
2. Verify your DISCORD_TOKEN is correct in `.env`
3. Ensure the bot is in the server you're testing in
4. Check bot logs for detailed error messages

---

Made with ❤️ for Discord
