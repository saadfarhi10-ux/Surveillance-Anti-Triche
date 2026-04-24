from dataclasses import dataclass


@dataclass
class SessionConfig:
    student_id: str
    subject: str
    duration_minutes: int
    webcam_index: int = 0
    confidence_threshold: float = 0.45
    offscreen_seconds: int = 10
    capture_on_alert: bool = True
    alert_cooldown_seconds: int = 8
