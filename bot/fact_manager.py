import json
import random
import os
from typing import Dict, List, Optional

class FactManager:
    """Manages loading and retrieving facts from JSON files"""
    
    def __init__(self, facts_directory: str = "data/facts"):
        self.facts_directory = facts_directory
        self.facts_cache = {}
        self.recent_facts = []  # Track recent facts to avoid immediate repeats
        self.max_recent_facts = 5  # Remember last 5 facts
        self.load_all_facts()
    
    def load_all_facts(self):
        """Load all fact files from the facts directory"""
        if not os.path.exists(self.facts_directory):
            print(f"Warning: Facts directory {self.facts_directory} not found!")
            return
        
        for filename in os.listdir(self.facts_directory):
            if filename.endswith('.json'):
                theme_name = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.facts_directory, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        theme_data = json.load(f)
                        self.facts_cache[theme_name] = theme_data.get('facts', [])
                        print(f"Loaded {len(self.facts_cache[theme_name])} facts for theme: {theme_name}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def get_random_fact(self, theme: Optional[str] = None) -> str:
        """Get a random fact from specified theme or all themes, avoiding recent repeats"""
        if not self.facts_cache:
            return "Sorry, no facts are available right now! 😅"
        
        if theme and theme in self.facts_cache:
            facts = self.facts_cache[theme]
            if not facts:
                return f"No facts available for theme '{theme}' yet! 🤔"
            
            # Try to avoid recent facts
            available_facts = [f for f in facts if f not in self.recent_facts]
            if not available_facts:  # If all facts were recent, use any fact
                available_facts = facts
            
            selected_fact = random.choice(available_facts)
            self._track_recent_fact(selected_fact)
            return selected_fact
        
        elif theme:
            # Theme not found
            available_themes = ", ".join(self.facts_cache.keys())
            return f"Theme '{theme}' not found! Available themes: {available_themes} 📚"
        
        else:
            # Random fact from any theme
            all_facts = []
            for theme_facts in self.facts_cache.values():
                all_facts.extend(theme_facts)
            
            if not all_facts:
                return "No facts available! Add some facts to get started! 📝"
            
            # Try to avoid recent facts
            available_facts = [f for f in all_facts if f not in self.recent_facts]
            if not available_facts:
                available_facts = all_facts
            
            selected_fact = random.choice(available_facts)
            self._track_recent_fact(selected_fact)
            return selected_fact
    
    def _track_recent_fact(self, fact: str):
        """Track recently used facts to avoid immediate repeats"""
        self.recent_facts.append(fact)
        if len(self.recent_facts) > self.max_recent_facts:
            self.recent_facts.pop(0)  # Remove oldest fact
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes"""
        return list(self.facts_cache.keys())
    
    def get_theme_fact_count(self, theme: str) -> int:
        """Get number of facts in a specific theme"""
        return len(self.facts_cache.get(theme, []))
    
    def add_fact(self, theme: str, fact: str) -> bool:
        """Add a new fact to a theme (and save to file)"""
        if theme not in self.facts_cache:
            self.facts_cache[theme] = []
        
        self.facts_cache[theme].append(fact)
        
        # Save to file
        try:
            file_path = os.path.join(self.facts_directory, f"{theme}.json")
            theme_data = {"theme": theme, "facts": self.facts_cache[theme]}
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving fact to {theme}: {e}")
            return False 