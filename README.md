# Discord Bot - Leaderboard & Curses

A fun Discord bot with a points leaderboard system and customizable "curse" effects for members!

## Features

### 🏆 Leaderboard System
- **Add/Remove Points**: Admins can award or deduct points from members
- **View Leaderboard**: Anyone can view the top players
- **Reset Leaderboard**: Admins can reset all data
- **Persistent Storage**: Data saved in SQLite database

### 🔥 Curse System (20 Types)

Admins can apply curses to members that modify how their messages appear:

**Text Effects:**
- `no_vowels` - All vowels are removed
- `no_e` - The letter 'e' cannot be used
- `reverse` - Messages are reversed
- `morse_code` - Converts to Morse code
- `pig_latin` - Converts to Pig Latin
- `upside_down` - Text is reversed and flipped
- `backwards_words` - Every word is spelled backwards

**Word Effects:**
- `shuffle` - Words have their letters shuffled
- `stutter` - Every letter is doubled
- `yoda_speak` - Word order is reversed
- `pirate_speak` - Speak like a pirate!
- `spelling_bee` - Every letter is separated
- `uwu_speak` - R's and L's become W's
- `doubletalk` - Every word is doubled and reversed

**Special Effects:**
- `emoji_prefix` - Random emoji added to messages
- `robotic` - SHOUT LIKE A ROBOT
- `slowmo` - Words are spelled out letter by letter
- `random_caps` - Random letters are capitalized
- `binary_prefix` - Messages have a binary prefix
- `math_curse` - **Must solve a math problem to send each message!**

**Curse Mechanics:**
- Auto-expire after specified duration
- Multiple curses can be applied to the same person
- Cursed messages are intercepted and transformed
- Math curse blocks all messages until equation is solved

## Commands

### Public Commands

```
/leaderboard [limit]
```
View the leaderboard. Optional limit parameter (default: 10)

```
/curses @member
```
View all active curses on a member

### Admin Commands

```
/give-points @member <points>
```
Add points to a member

```
/remove-points @member <points>
```
Remove points from a member

```
/reset-leaderboard
```
Reset all leaderboard data (requires confirmation)

```
/curse @member <curse_type> <hours>
```
Apply a curse to a member for specified duration

```
/lift-curse @member
```
Remove all curses from a member

## Setup

### Requirements
- Python 3.10+
- discord.py 2.3.2
- python-dotenv

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JellyGirl884/Bleh.git
   cd Bleh
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**
   ```bash
   echo "DISCORD_TOKEN=your_token_here" > .env
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Getting Your Discord Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to **Bot** section → **Add Bot**
4. Under **TOKEN**, click "Copy" to get your token
5. Paste it in your `.env` file

### Inviting the Bot to Your Server

1. Go to **OAuth2** → **URL Generator**
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: `Send Messages`, `Read Messages/View Channels`, `Manage Messages`, `Embed Links`
4. Copy the generated URL and open it in your browser

## Project Structure

```
Bleh/
├── main.py              # Bot initialization
├── database.py          # SQLite database management
├── curses.py            # Curse effects and math problems
├── cogs/
│   ├── leaderboard.py   # Leaderboard commands
│   └── curses.py        # Curse application and handling
├── data/
│   └── leaderboard.db   # SQLite database (auto-created)
├── requirements.txt     # Python dependencies
├── .env                 # Discord token (create this)
├── .gitignore           # Git ignore rules
└── README.md           # This file
```

## How It Works

### Leaderboard
- Points are stored in SQLite database
- Admins can modify points with commands
- Leaderboard is sorted by points (highest first)
- All members visible with medals (🥇🥈🥉)

### Curses
- When a curse is applied, it's stored with expiration time
- When cursed user sends a message:
  - For **math curse**: Message is deleted, user prompted with equation
  - For **other curses**: Message is deleted, replaced with transformed version
- Curses auto-expire based on stored timestamp
- Multiple curses on same user: first curse in system takes priority

## Permissions

- **Leaderboard**: Everyone can view
- **Points/Reset**: Admin only
- **Curses**: Admin only to apply/lift
- **View Curses**: Everyone can check active curses

## Database Schema

### leaderboard table
```sql
CREATE TABLE leaderboard (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    points INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### curses table
```sql
CREATE TABLE curses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    curse_type TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1
)
```

## Troubleshooting

### Bot not responding
- Check Discord token in `.env` file
- Verify bot has proper permissions in server
- Check console for error messages

### Commands not appearing
- Ensure bot has `applications.commands` scope
- Restart bot to sync commands
- Check bot has "Send Messages" permission

### Curses not working
- Verify bot has "Manage Messages" permission
- Check user has active curses with `/curses @user`
- Ensure curse hasn't expired

## License

Feel free to use and modify this bot!

## Support

For issues or questions, create a GitHub issue in this repository.
