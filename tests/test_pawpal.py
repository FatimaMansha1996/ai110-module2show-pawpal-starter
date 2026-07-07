"""Tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Task, Priority


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's completed status to True."""
    task = Task("Walk", 30, Priority.HIGH)
    assert task.completed is False  # tasks start incomplete

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0  # a new pet has no tasks

    pet.add_task(Task("Feeding", 10, Priority.MEDIUM))

    assert len(pet.tasks) == 1
