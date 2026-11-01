# Monster Hunter Wilds Crafting & Crown Checklist

An endgame Armor, Charms, and Weapons tracker as well as a Mini and Large crown monster tracker.

---

## Key Features

* **Endgame Equipment Tracking:** Dynamically extracts and maps Rarity 6+ Armor sets, Rarity 8 weapons grouped by weapon class, and maxed-tier Charms.
* **Gold Crown Progressor:** Automatically calculates and displays mini and large crown achievements across non-fixed size large monsters.
* **State Persistence:** Automatically saves your checked boxes to a localized tracking file (`checklist_progress.json`), ensuring your data stays safe across app launches and restarts.

---

## Required Directory Structure

For the tracker to parse data correctly, your root directory must contain a `jsons` folder with your extracted Monster Hunter Wilds dataset arranged as follows:

```text
├── MHWildsChecklist.py       # Main application logic
├── run_dashboard.py            # Executable launcher wrapper
├── jsons/
│   ├── Armor.json            # Base armor definitions
│   ├── Amulet.json           # Charm tree variants
│   ├── LargeMonsters.json    # Monster base data & size constraints
│   └── weapons/
│       ├── GreatSword.json
│       ├── LongSword.json
│       └── [OtherWeaponTypes].json
```

---

## Requirements

The following is required for the tracker to run:

[Python 3.11+](https://www.python.org/)

[Streamlit Latest Stable Version](https://streamlit.io)

optionals:

If you want to turn this project into an executable you will need the following:

[pyinstaller 6.0.0+](https://pyinstaller.org)

---

## Running the Tracker

After installing the requirements above:
1. Open your command console
2. Change directory to the project folder
3. Run 'python run_dashboard.py'

After running the command, your default web browser will open to display the tracker. (Usually at http:localhost:8501)

---

## Shoutouts
Big thanks to [LartTyler](https://github.com/LartTyler) for the [mhdb-wilds-data](https://github.com/LartTyler/mhdb-wilds-data) repo, which provided the JSON files used in this project.
