"""Session persistence and management."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from models import Session, SessionListItem, SessionStatus, BudgetInfo
from config import get_settings


class SessionManager:
    """Manages session persistence to JSON files."""
    
    def __init__(self):
        settings = get_settings()
        self.sessions_dir = Path(settings.sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_session_path(self, session_id: str) -> Path:
        """Get the file path for a session."""
        return self.sessions_dir / f"{session_id}.json"
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"anj-{timestamp}"
    
    def save_session(self, session: Session) -> None:
        """Save a session to disk."""
        session.updated_at = datetime.now()
        session_path = self._get_session_path(session.session_id)
        
        with open(session_path, 'w', encoding='utf-8') as f:
            json.dump(session.model_dump(mode='json'), f, indent=2, default=str)
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """Load a session from disk."""
        session_path = self._get_session_path(session_id)
        
        if not session_path.exists():
            return None
        
        with open(session_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Session(**data)
    
    def list_sessions(self) -> list[SessionListItem]:
        """List all sessions."""
        sessions = []
        
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    sessions.append(SessionListItem(
                        session_id=data['session_id'],
                        created_at=data['created_at'],
                        issue=data['issue'],
                        status=data['status'],
                        total_cost=data['budget']['used'],
                        iteration_count=len(data.get('iterations', []))
                    ))
            except Exception as e:
                print(f"Error loading session {session_file}: {e}")
                continue
        
        # Sort by creation date, newest first
        sessions.sort(key=lambda x: x.created_at, reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        session_path = self._get_session_path(session_id)
        
        if session_path.exists():
            session_path.unlink()
            return True
        return False
    
    def update_session_status(self, session_id: str, status: SessionStatus) -> None:
        """Update session status."""
        session = self.load_session(session_id)
        if session:
            session.status = status
            self.save_session(session)

