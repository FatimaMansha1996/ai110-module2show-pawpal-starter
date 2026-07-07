"""PawPal+ logic layer.

Backend classes for the pet care planning assistant. This is the "skeleton":
class names, attributes, and empty method stubs based on the UML in
diagrams/DraftUML.mmd. Implement the method bodies in later steps.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    start_time: str | None = None  # set by the scheduler once planned


@dataclass
class Pet:
    """A single animal owned by the user."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        ...


@dataclass
class Owner:
    """The pet owner and entry point for the app."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet with this owner."""
        ...


class Scheduler:
    """Builds and explains a daily care plan from a set of tasks."""

    def __init__(self, available_minutes: int) -> None:
        self.available_minutes = available_minutes

    def build_plan(self, tasks: list[Task]) -> list[Task]:
        """Order/select tasks into a daily plan based on priority and time."""
        ...

    def explain(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        ...
