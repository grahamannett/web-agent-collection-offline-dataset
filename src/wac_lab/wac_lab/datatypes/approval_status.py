from typing import NamedTuple


class _ApprovalStatus(NamedTuple):
    color: str
    emoji: str


Approved = _ApprovalStatus("green", "✅")
Rejected = _ApprovalStatus("red", "❌")
Running = _ApprovalStatus("purple", "🏃🏻‍♀️")
Pending = _ApprovalStatus("orange", "👾")

DefaultStatus = Pending
