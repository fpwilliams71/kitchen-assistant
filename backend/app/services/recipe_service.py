from typing import List, Dict, Optional
import json
import sqlite3
from pathlib import Path

class RecipeService:
    def __init__(self, db_path: str = "recipes.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize recipe database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                cooking_time INTEGER,
                difficulty TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_saved_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                user_notes TEXT,
                rating INTEGER,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_recipe(self, recipe_data: Dict) -> bool:
        """Save a recipe to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO recipes (name, ingredients, instructions, cooking_time, difficulty)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                recipe_data['name'],
                json.dumps(recipe_data['ingredients']),
                recipe_data['instructions'],
                recipe_data.get('cooking_time', 30),
                recipe_data.get('difficulty', 'medium')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving recipe: {e}")
            return False

recipe_service = RecipeService()