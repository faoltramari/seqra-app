# NY SEQRA Classification System (Genesee County, NY)

A standalone, web-based decision support tool built with **Python** and **Streamlit** to automate environmental review classifications under **6 NYCRR Part 617 (State Environmental Quality Review Act - SEQRA)**. Optimized for municipal planning boards, code enforcement, and land use administration in Genesee County and across New York State.

---

## 🏛️ Project Overview
Manually cross-referencing SEQRA regulations for complex projects involving mixed-use footprints, agricultural districts, and historic overlays can lead to evaluation bottlenecks or logical errors. This application provides a deterministic, transparent, and holistic rules engine that evaluates project parameters simultaneously to determine whether an action is **Type I**, **Type II**, or **Unlisted**.

## 🚀 Key Features & Regulatory Logic
* **Holistic Evaluation Engine:** Processes all inputs simultaneously rather than sequentially, preventing the system from prematurely "locking in" on exemptions.
* **Statutory Precedence Enforcement:** Automatically ensures that major **Type I thresholds** (e.g., 10+ acres of physical disturbance) legally supersede and override minor **Type II exemptions** (e.g., small building footprints).
* **Contextual Overlay Thresholds:** Implements the statutory **25% threshold rule** for projects located within Certified Agricultural Districts (`617.4(b)(8)`), contiguous to Historic Sites (`617.4(b)(9)`), or contiguous to Public Parkland (`617.4(b)(10)`).
* **Mixed-Use Guardrails:** Automatically prevents substantial commercial/non-residential footprints ($\ge$ 4,000 sq. ft.) from mistakenly claiming pure residential Type II exemptions (`617.5(c)(11)`).

---

## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Streamlit (for interactive web UI)
* **Hosting / Deployment:** Streamlit Community Cloud (embeddable via iframe into municipal CMS platforms like Granicus OpenCities)

---

## 💻 Local Installation & Execution

To run this application locally on your machine:

1. **Clone or download** this repository to your local directory.
2. Open your terminal or command prompt inside the project folder (`SeqraApp`).
3. Ensure **Streamlit** is installed in your Python environment:
   ```cmd
   pip install streamlit
