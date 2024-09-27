from typing import NamedTuple


class ApprovalStatus(NamedTuple):
    name: str
    color: str
    emoji: str


Approved = ApprovalStatus("approved", "green", "✅")
Rejected = ApprovalStatus("rejected", "red", "❌")
Running = ApprovalStatus("running", "purple", "🏃🏻‍♀️")
Pending = ApprovalStatus("pending", "orange", "👾")

DefaultStatus = Pending
