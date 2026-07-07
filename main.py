"""Temporary testing ground for PawPal+ logic.

Run with:  python main.py

Builds a small scenario (one owner, two pets, several tasks) and prints
today's schedule to the terminal so we can verify the logic works.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency


def main() -> None:
    # 1. Create an owner and at least two pets.
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    biscuit = Pet("Biscuit", "cat")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # 2. Add at least three tasks with different durations/priorities.
    mochi.schedule_walk(duration_minutes=30, priority=Priority.HIGH)
    mochi.add_task(Task("Feeding", 10, Priority.HIGH, Frequency.DAILY))
    biscuit.add_task(Task("Medication", 5, Priority.MEDIUM, Frequency.DAILY))
    biscuit.add_task(Task("Enrichment play", 20, Priority.LOW, Frequency.WEEKLY))

    # 3. Build today's schedule across all of the owner's pets.
    scheduler = Scheduler(available_minutes=120, day_start="08:00")
    scheduler.plan_for_owner(owner)

    # 4. Print "Today's Schedule" to the terminal.
    print("=" * 40)
    print(f"  Today's Schedule for {owner.name}")
    print("=" * 40)
    print(scheduler.format_plan())


if __name__ == "__main__":
    main()
