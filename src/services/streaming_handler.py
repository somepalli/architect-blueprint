"""
Service for managing real-time updates to the Streamlit UI.
"""
from typing import Dict, Any, Optional
from datetime import datetime


class StreamingUpdate:
    """Represents a single streaming update."""

    def __init__(
        self,
        phase: str,
        phase_index: int,
        reasoning: str,
        progress: float,
        diagram: Optional[str] = None,
        data: Optional[Any] = None,
        status: str = "in_progress",
    ):
        self.phase = phase
        self.phase_index = phase_index
        self.reasoning = reasoning
        self.progress = progress
        self.diagram = diagram
        self.data = data
        self.status = status
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy serialization."""
        return {
            "phase": self.phase,
            "phase_index": self.phase_index,
            "reasoning": self.reasoning,
            "progress": self.progress,
            "diagram": self.diagram,
            "data": self.data,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }


class StreamingHandler:
    """Manages streaming updates for real-time UI updates."""

    PHASES = [
        "Requirements Analysis",
        "Database Schema",
        "API Design",
        "Frontend Architecture",
        "Deployment Plan",
    ]

    def __init__(self):
        self.current_phase_index = 0
        self.updates = []

    def create_update(
        self,
        phase: str,
        reasoning: str,
        diagram: Optional[str] = None,
        data: Optional[Any] = None,
        status: str = "in_progress",
    ) -> StreamingUpdate:
        """
        Create a streaming update.

        Args:
            phase: Current phase name
            reasoning: Agent reasoning/explanation
            diagram: Optional Mermaid diagram
            data: Optional data payload
            status: Status (in_progress, completed, error)

        Returns:
            StreamingUpdate object
        """
        # Find phase index
        phase_index = 0
        for idx, phase_name in enumerate(self.PHASES):
            if phase_name.lower() in phase.lower():
                phase_index = idx
                self.current_phase_index = idx
                break

        # Calculate progress (0-100)
        progress = (self.current_phase_index / len(self.PHASES)) * 100
        if status == "completed":
            progress = ((self.current_phase_index + 1) / len(self.PHASES)) * 100

        update = StreamingUpdate(
            phase=phase,
            phase_index=phase_index,
            reasoning=reasoning,
            progress=progress,
            diagram=diagram,
            data=data,
            status=status,
        )

        self.updates.append(update)
        return update

    def get_progress_percentage(self) -> float:
        """Get current progress percentage."""
        return (self.current_phase_index / len(self.PHASES)) * 100

    def get_phase_status(self, phase_index: int) -> str:
        """
        Get status of a specific phase.

        Returns: 'completed', 'in_progress', or 'pending'
        """
        if phase_index < self.current_phase_index:
            return "completed"
        elif phase_index == self.current_phase_index:
            return "in_progress"
        else:
            return "pending"

    def format_reasoning(self, phase: str, reasoning: str) -> str:
        """
        Format reasoning text for display.

        Args:
            phase: Current phase
            reasoning: Raw reasoning text

        Returns:
            Formatted markdown text
        """
        return f"""### {phase}

{reasoning}

---
"""

    def get_phase_emoji(self, phase_index: int) -> str:
        """Get emoji for phase status."""
        status = self.get_phase_status(phase_index)
        if status == "completed":
            return "✅"
        elif status == "in_progress":
            return "🔄"
        else:
            return "⏸️"

    def get_phase_timeline(self) -> str:
        """Get formatted phase timeline."""
        lines = []
        for idx, phase in enumerate(self.PHASES):
            emoji = self.get_phase_emoji(idx)
            lines.append(f"{emoji} {phase}")
        return "\n".join(lines)

    def reset(self):
        """Reset handler state."""
        self.current_phase_index = 0
        self.updates = []
