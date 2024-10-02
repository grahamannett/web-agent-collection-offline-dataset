from enum import Enum


class ApprovalStatus(Enum):
    APPROVED = ("approved", "green", "✅")
    REJECTED = ("rejected", "red", "❌")
    RUNNING = ("running", "purple", "🏃🏻‍♀️")
    PENDING = ("pending", "orange", "👾")

    def __init__(self, approval_type: str, color: str, emoji: str):
        self.approval_type = approval_type
        self.color = color
        self.emoji = emoji


DefaultStatus = ApprovalStatus.PENDING


if __name__ == "__main__":
    running = ApprovalStatus.RUNNING
    assert running.color == "purple"
