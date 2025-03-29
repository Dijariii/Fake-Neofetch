import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class ProfileManager:
    def __init__(self):
        self.profiles_dir = os.path.join("resources", "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.profiles: Dict[str, Dict] = {}
        self.load_profiles()

    def load_profiles(self) -> None:
        """Load all profiles from the profiles directory"""
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".json"):
                profile_name = os.path.splitext(filename)[0]
                profile = self.load_profile(profile_name)
                if profile:
                    self.profiles[profile_name] = profile

    def get_profiles(self) -> List[str]:
        """Get list of available profile names"""
        profiles = []
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".json"):
                profiles.append(filename[:-5])  # Remove .json extension
        return sorted(profiles)

    def load_profile(self, name: str) -> Optional[Dict]:
        """Load a profile by name"""
        filepath = os.path.join(self.profiles_dir, f"{name}.json")
        if not os.path.exists(filepath):
            return None
            
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception:
            return None

    def save_profile(self, name: str, profile_data: Dict):
        """Save a profile"""
        filepath = os.path.join(self.profiles_dir, f"{name}.json")
        with open(filepath, "w") as f:
            json.dump(profile_data, f, indent=4)

    def delete_profile(self, name: str):
        """Delete a profile"""
        filepath = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(filepath):
            os.remove(filepath)

    def get_profile(self, name: str) -> Optional[Dict]:
        """Get a profile by name (alias for load_profile)"""
        return self.load_profile(name)

    def get_all_profiles(self) -> List[str]:
        """Get list of all profile names"""
        return list(self.profiles.keys())

    def update_profile(self, name: str, info: Dict[str, str]) -> None:
        """Update an existing profile"""
        if name in self.profiles:
            self.profiles[name]["info"].update(info)
            self.profiles[name]["last_modified"] = datetime.now().isoformat()
            self.save_profile(name, self.profiles[name]["info"])

    def get_profile_metadata(self, name: str) -> Optional[Dict]:
        """Get profile metadata including creation and modification dates"""
        if name in self.profiles:
            return {
                "name": self.profiles[name]["name"],
                "created_at": self.profiles[name]["created_at"],
                "last_modified": self.profiles[name]["last_modified"]
            }
        return None

    def duplicate_profile(self, source_name: str, new_name: str) -> None:
        """Create a duplicate of an existing profile with a new name"""
        if source_name in self.profiles:
            source_profile = self.profiles[source_name]
            new_profile = {
                "name": new_name,
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat(),
                "info": source_profile["info"].copy()
            }
            self.save_profile(new_name, new_profile["info"])

    def export_profile(self, name: str, export_path: str) -> None:
        """Export a profile to a specified path"""
        if name in self.profiles:
            with open(export_path, "w") as f:
                json.dump(self.profiles[name], f, indent=4)

    def import_profile(self, filepath: str) -> bool:
        """Import a profile from a JSON file"""
        try:
            with open(filepath, "r") as f:
                profile_data = json.load(f)
                if "name" not in profile_data:
                    return False
                self.save_profile(profile_data["name"], profile_data)
                return True
        except Exception:
            return False 