# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

a. Initial design

My initial UML centered on four classes, each owning one clear responsibility:

Owner — represents the pet owner. Holds basic info (name) and their list of pets. Responsible for owning pets and, through them, the tasks that need scheduling. This is the entry point for the "add a pet" flow.

Pet — represents a single animal (name, species). Responsible for holding its own care tasks and identifying itself in the schedule ("Morning walk — Mochi"). A Pet is created and attached to an Owner when the user adds a pet.

Task — represents one care activity (title, duration in minutes, priority, and eventually a scheduled start time). Responsible for describing what needs to happen and carrying the attributes the scheduler sorts on. "Schedule a walk" creates a Task with title "Walk", a duration, and a priority.

Scheduler — the brain. Responsible for taking a list of Task objects plus constraints (available time in the day, priorities) and producing an ordered daily plan. It sorts tasks by priority, fits them into the available time, drops or flags tasks that don't fit, and can explain why each was chosen. "See today's tasks" calls the scheduler and displays its output.

Relationships:

Owner "1" --> "*" Pet (an owner has many pets)
Pet "1" --> "*" Task (a pet has many care tasks)
Scheduler --> Task (the scheduler reads and orders tasks to build the daily plan)
I separated Task from Scheduler on purpose: a Task is just data about one activity, while the Scheduler holds all the decision logic. That keeps the scheduling rules in one place and makes the tasks easy to test and reuse.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
