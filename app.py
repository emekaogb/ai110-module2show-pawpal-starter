import streamlit as st
from pawpal_system import Owner, Task, Pet, Schedule, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pet" not in st.session_state:
    st.session_state.pet = None

if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule(time_budget=120)

# --- Owner + Pet setup ---
st.subheader("Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    owner_email = st.text_input("Owner email", value="jordan@email.com")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    owner = Owner(name=owner_name, email=owner_email)
    pet = Pet(name=pet_name, animal=species)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.session_state.schedule = Schedule(time_budget=120)
    st.session_state.schedule.add_pet(pet)
    st.success(f"Saved {owner_name} and {pet_name} the {species}.")

if st.session_state.owner and st.session_state.pet:
    col1, col2 = st.columns(2)
    col1.metric("Owner", st.session_state.owner.name)
    col2.metric("Pet", f"{st.session_state.pet.name} ({st.session_state.pet.animal})")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])

if st.button("Add Task"):
    if st.session_state.pet is None:
        st.error("Save an owner and pet first.")
    else:
        priority_map = {
            "low": Priority.LOW,
            "medium": Priority.MEDIUM,
            "high": Priority.HIGH,
        }
        task = Task(
            name=task_title,
            duration=int(duration),
            priority=priority_map[priority_str],
            frequency=frequency,
        )
        st.session_state.pet.add_task(task)
        st.success(f"Task added: **{task_title}** ({duration} min, {priority_str} priority)")

# --- Current task list ---
if st.session_state.pet and st.session_state.pet.tasks:
    tasks = st.session_state.pet.tasks
    pending = [t for t in tasks if not t.completed]
    done = [t for t in tasks if t.completed]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", len(tasks))
    col2.metric("Pending", len(pending))
    col3.metric("Completed", len(done))

    priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
    st.dataframe(
        [
            {
                "Task": t.name,
                "Duration (min)": t.duration,
                "Priority": f"{priority_icon.get(t.priority.name, '')} {t.priority.name}",
                "Frequency": t.frequency,
                "Done": "✓" if t.completed else "—",
            }
            for t in tasks
        ],
        use_container_width=True,
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

col1, col2 = st.columns(2)
with col1:
    time_budget = st.number_input("Time budget (minutes)", min_value=10, max_value=480, value=120)
with col2:
    sort_order = st.selectbox("Sort by duration", ["none", "shortest first", "longest first"])

if st.button("Generate Schedule"):
    if st.session_state.pet is None or not st.session_state.pet.tasks:
        st.error("Add an owner, pet, and at least one task first.")
    else:
        st.session_state.schedule.time_budget = time_budget
        result = st.session_state.schedule.schedule_all_tasks()

        if not result:
            st.warning("No tasks fit within the time budget. Try increasing it.")
        else:
            if sort_order == "shortest first":
                result = st.session_state.schedule.sort_by_time(reverse=False)
            elif sort_order == "longest first":
                result = st.session_state.schedule.sort_by_time(reverse=True)

            total = sum(e["duration"] for e in result)
            skipped = len(st.session_state.pet.tasks) - len(result)

            st.success(f"Schedule generated — {len(result)} tasks, {total} min planned.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Tasks Scheduled", len(result))
            col2.metric("Time Used (min)", total)
            col3.metric("Tasks Skipped", skipped, delta=f"-{skipped}" if skipped else None,
                        delta_color="inverse")

            priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            st.dataframe(
                [
                    {
                        "Start (min)": e["start_time"],
                        "Pet": e["pet"],
                        "Task": e["task"],
                        "Duration (min)": e["duration"],
                        "Priority": f"{priority_icon.get(e['priority'].name, '')} {e['priority'].name}",
                    }
                    for e in result
                ],
                use_container_width=True,
            )

            conflicts = st.session_state.schedule.detect_conflicts()
            if conflicts:
                st.warning(f"{len(conflicts)} conflict(s) detected in the schedule:")
                for a, b in conflicts:
                    st.write(f"- **{a['pet']} / {a['task']}** overlaps with **{b['pet']} / {b['task']}**")
            else:
                st.success("No scheduling conflicts detected.")
