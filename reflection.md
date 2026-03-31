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

I used Claude in every stage of the process. When I was designing and brainstorming, I prompted Claude to build a Mermaid.js diagram that helped me visualize what the system was going to do and how the object classes interacted with one another. Then when I was implementing, debugging and refactoring; I was able to use AI to generate a skeleton for each class and their respective methods, and then iteratively build from there. The most helpful prompts were the ones that provided a lot of detail and context for what was to be accomplished. 

**b. Judgment and verification**

I didn't accept AI's suggestion when it told me to used a more optimized code block for the detect_conflicts() method because I thought it was extremely unreadable and would be hard for a human to understand or debug later on. I was able to evaluate because I was on the "Ask before edits" mode.
---

## 4. Testing and Verification

**a. What you tested**

I tested:
- Pet.complete_task(): to make sure that recurring tasks were requeued based on their frequency (daily, weekly, monthly).
- Schedule.schedule_all_tasks(): to make sure it respects the time budget provided.
- Schedule.detect_conflicts(): because I had it refactored for readability and needed to make sure it correctly identified overlapping windows. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

I was surprised that I was able to build an entire system in a couple hours using AI tools. I think these tools enable smaller teams to create something that could have large-scale impact. 

**b. What you would improve**

If I were to start over, I would be more specific upfront about the different intricacies of the system I'm trying to build, rather than only having 4 classes and a couple methods to start with. 

**c. Key takeaway**

I learned that designing with AI requires discernment and attention to detail. I understand more now what they mean when they say there needs to be a human in the loop. 
