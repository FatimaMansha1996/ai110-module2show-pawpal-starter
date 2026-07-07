"""PawPal+ logic layer.

Backend classes for the pet care planning assistant, based on the UML in
diagrams/DraftUML.mmd:

- Task      : a single care activity (description, time, frequency, completion)
- Pet       : pet details plus its list of tasks
- Owner     : manages multiple pets and exposes all their tasks
- Scheduler : the "brain" that retrieves, organizes, and orders tasks across pets
"""

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class Priority(IntEnum):
    """Task priority. Higher value = more important, so tasks sort cleanly."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Frequency(str, Enum):
    """How often a task recurs."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.DAILY
    completed: bool = False
    start_time: str | None = None  # "HH:MM", assigned by the scheduler once planned
    pet_name: str | None = None  # set when the task is added to a pet

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def __str__(self) -> str:
        who = f" — {self.pet_name}" if self.pet_name else ""
        when = f"{self.start_time} " if self.start_time else ""
        done = " ✓" if self.completed else ""
        return (
            f"{when}{self.title}{who} "
            f"({self.duration_minutes} min) [priority: {self.priority.name.lower()}]{done}"
        )


@dataclass
class Pet:
    """A single animal owned by the user, holding its own care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def schedule_walk(
        self, duration_minutes: int = 30, priority: Priority = Priority.HIGH
    ) -> Task:
        """Core action: create a walk Task, add it to this pet, and return it."""
        walk = Task(
            title="Walk",
            duration_minutes=duration_minutes,
            priority=priority,
            frequency=Frequency.DAILY,
        )
        self.add_task(walk)
        return walk

    def pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """The pet owner: manages multiple pets and access to all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Core action: register a new pet with this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Flatten every task across all of this owner's pets into one list."""
        return [task for pet in self.pets for task in pet.tasks]

    def pending_tasks(self) -> list[Task]:
        """All not-yet-completed tasks across every pet."""
        return [task for task in self.all_tasks() if not task.completed]


class Scheduler:
    """Builds and explains a daily care plan from a set of tasks."""

    def __init__(self, available_minutes: int = 240, day_start: str = "08:00") -> None:
        self.available_minutes = available_minutes
        self.day_start = day_start
        self.plan: list[Task] = []  # last plan built, so explain() has something to describe
        self.skipped: list[Task] = []  # tasks that did not fit in the time budget

    def build_plan(self, tasks: list[Task]) -> list[Task]:
        """Order and select tasks into a daily plan by priority, then fit into time.

        Highest priority first (ties broken by shorter duration so more tasks fit),
        assigning each selected task a start_time until the time budget runs out.
        """
        ordered = sorted(
            tasks, key=lambda t: (-int(t.priority), t.duration_minutes)
        )

        self.plan = []
        self.skipped = []
        clock = self._to_minutes(self.day_start)
        remaining = self.available_minutes

        for task in ordered:
            if task.duration_minutes <= remaining:
                task.start_time = self._to_hhmm(clock)
                clock += task.duration_minutes
                remaining -= task.duration_minutes
                self.plan.append(task)
            else:
                task.start_time = None
                self.skipped.append(task)

        return self.plan

    def plan_for_owner(self, owner: Owner) -> list[Task]:
        """Retrieve all pending tasks from the owner's pets and build a plan."""
        return self.build_plan(owner.pending_tasks())

    def see_todays_tasks(self, pet: Pet) -> list[Task]:
        """Core action: build and return today's ordered plan for a single pet."""
        return self.build_plan(pet.pending_tasks())

    def explain(self) -> str:
        """Return a human-readable explanation of the most recent plan."""
        if not self.plan and not self.skipped:
            return "No plan has been built yet."

        lines = [
            f"Daily plan ({self.available_minutes} min available, "
            f"starting {self.day_start}):"
        ]
        for task in self.plan:
            lines.append(
                f"  {task.start_time} — {task.title}"
                + (f" ({task.pet_name})" if task.pet_name else "")
                + f" [{task.duration_minutes} min, {task.priority.name.lower()} priority]"
            )
        if self.skipped:
            lines.append("Skipped (not enough time):")
            for task in self.skipped:
                lines.append(
                    f"  {task.title}"
                    + (f" ({task.pet_name})" if task.pet_name else "")
                    + f" [{task.duration_minutes} min, {task.priority.name.lower()} priority]"
                )
        return "\n".join(lines)

    def format_plan(self) -> str:
        """Render the most recent plan as an aligned, scannable table."""
        if not self.plan and not self.skipped:
            return "No plan has been built yet."

        # Size the variable-width columns to their longest value (or header).
        task_w = max([len("TASK")] + [len(t.title) for t in self.plan])
        pet_w = max([len("PET")] + [len(t.pet_name or "") for t in self.plan])

        header = (
            f"  {'TIME':<5}  {'TASK':<{task_w}}  {'PET':<{pet_w}}  "
            f"{'DUR':>4}  PRIORITY"
        )
        separator = (
            f"  {'-' * 5}  {'-' * task_w}  {'-' * pet_w}  {'-' * 4}  {'-' * 8}"
        )

        lines = [header, separator]
        for t in self.plan:
            lines.append(
                f"  {t.start_time:<5}  {t.title:<{task_w}}  "
                f"{(t.pet_name or ''):<{pet_w}}  {f'{t.duration_minutes}m':>4}  "
                f"{t.priority.name}"
            )

        planned = sum(t.duration_minutes for t in self.plan)
        lines.append("")
        lines.append(f"  Total: {planned}m planned / {self.available_minutes}m available")

        if self.skipped:
            skipped = ", ".join(f"{t.title} ({t.pet_name})" for t in self.skipped)
            lines.append(f"  Skipped: {skipped}")
        else:
            lines.append("  Skipped: (none)")

        return "\n".join(lines)

    @staticmethod
    def _to_minutes(hhmm: str) -> int:
        hours, minutes = hhmm.split(":")
        return int(hours) * 60 + int(minutes)

    @staticmethod
    def _to_hhmm(total_minutes: int) -> str:
        return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"
