

<div align="center">

<img src="data/icons/hicolor/scalable/apps/io.github.Nu_nik_kak_nik.Numo.svg" width="128" height="128" alt="Numo icon">


# Numo


**Fast mental math training**

<img src="/data/screenshots/readme.png" width="325" height="375" alt="Main page">

</div>

## About project 🖩
Numo is a small GNOME app for training mental arithmetic. It generates
tasks on the fly and checks your answers instantly — no distraction, just numbers.


### Game modes
- **Normal**: an endless run of tasks that ends the moment you make a mistake. A test of focus and consistency.
- **Timer**: a fixed countdown. Solve as many tasks as you can before time runs out.
- **Timer + Bonus**: start with a small amount of time and earn extra seconds for every correct answer. The pace accelerates as you go.
- **Task Count**: a set number of tasks to solve. A clear goal to reach at your own pace. 

### Difficulty levels
- **Easy**: addition and subtraction.
- **Medium**: adds multiplication and exact division.
- **Hard**: negative numbers, floor div, and mod. 

### Statistics
Every session is recorded: result, accuracy, and time spent. The
statistics screen shows your best results per mode and difficulty,
recent games. Data can be exported and imported
as JSON at any time.
  
## My first project 🌟
This is my first GNOME application built with GTK4 and libadwaita. I'm using it as an opportunity to learn modern GNOME development practices.

Because of that, the codebase is deliberately kept and small readable.
If you spot something that could be done better according to the GNOME way, I'd be glad to hear about it.
  
## Roadmap 🗺️
  
The list below is not a rigid schedule, but merely an outline of the directions in which I would like to move.

### Difficulty
  - **Difficulty icons**:  add symbolic icons for each level (Easy, Medium, Hard) so the current setting is visible at a glance.
  - **Flexible difficulty settings**: allow customizing what each level does: which operations are included, number ranges, whether negative results are allowed. Right now the rules are hardcoded.
  
### Statistics
  - **Configurable number of recent matches**:  let the user choose how many sessions the "Recent" section shows.
  - **Redesign of the recent matches list**:  cleaner layout.
  
### Modes
  - **New game modes**: no concrete ideas yet. Candidate: "Reverse" (given the result, find the expression). Open to suggestions.
  
### Localization
  - **Prepare the project for translations** 

## License

Numo is distributed under the terms of the GNU General Public License,
version 3 or later. See [COPYING](COPYING) for details.
