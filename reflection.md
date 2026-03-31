# PawPal+ Project Reflection

## 1. System Design

*Core Actions:*
1. Add a pet.
2. Schedule a walk.
3. See today's tasks.

*Objects:*
- Owner (attributes: [name, email, image])
- Pet (attributes: [name, animal, image, tasks], methods: [init, add_task, update_pet, ])
- Task (attributes: [name, duration, priority, frequency], methods: [init, update_task, ])
- Schedule (attributes: [schedule, pets], methods: [init, schedule_all_tasks, ])

**a. Initial design**

There is one owner. The Pet object has a list of tasks. The Task object has name, duration, priority and frequency to be used for scheduling purposes. The Schedule object takes in a list of pets

**b. Design changes**

I added the add_pet() method to the Schedule object class so that if a new pet needs to be accounted for, a whole new object doesn't need to be created. I also made priority on Task an enum based on the AI's suggestion.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers duration, priority and frequency that the task needs to be performed when creating the schedule. I decided these mattered the most because they determine when a task could and should be scheduled vs. what is preferred which can be added later if necessary.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff was that the detect conflicts method runs in O(N-squared) because I wanted the logic to be more readable as opposed to optimized. Since, the system will nly be used to small, practical examples, I figured it should be fine for now, and optimization can come later.

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
