import sqlite3
import os
from datetime import datetime

DB_PATH = "data/leaderboard.db"

def init_db():
    """Initialize the database"""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create leaderboard table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create curses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            curse_type TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()

def add_or_update_points(user_id, username, points):
    """Add or update a user's points"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO leaderboard (user_id, username, points)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        points = points + ?,
        username = ?,
        last_updated = CURRENT_TIMESTAMP
    """, (user_id, username, points, points, username))
    
    conn.commit()
    conn.close()

def get_leaderboard(limit=None):
    """Get leaderboard sorted by points (descending)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT user_id, username, points FROM leaderboard
            ORDER BY points DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT user_id, username, points FROM leaderboard
            ORDER BY points DESC
        """)
    
    results = cursor.fetchall()
    conn.close()
    return results

def reset_leaderboard():
    """Reset all leaderboard data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM leaderboard")
    cursor.execute("DELETE FROM curses")
    
    conn.commit()
    conn.close()

def add_curse(user_id, curse_type, expires_at):
    """Add a curse to a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO curses (user_id, curse_type, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, curse_type, expires_at))
    
    conn.commit()
    conn.close()

def get_active_curses(user_id):
    """Get all active curses for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, curse_type, expires_at FROM curses
        WHERE user_id = ? AND is_active = 1 AND expires_at > CURRENT_TIMESTAMP
        ORDER BY expires_at ASC
    """, (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def expire_curses(user_id):
    """Mark expired curses as inactive"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE curses
        SET is_active = 0
        WHERE user_id = ? AND expires_at <= CURRENT_TIMESTAMP
    """, (user_id,))
    
    conn.commit()
    conn.close()

def remove_all_curses(user_id):
    """Remove all curses from a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE curses
        SET is_active = 0
        WHERE user_id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()
