import streamlit as st
import json
import os
import glob

#Save file for tracking progress
PROGRESS_FILE = "checklist_progress.json"
BASE_ROOT = os.path.dirname(os.path.abspath(__file__))
ABS_PROGRESS_FILE = os.path.join(BASE_ROOT, PROGRESS_FILE)

st.set_page_config(page_title="MH Wilds Checklist", layout="wide")

if "user_checks" not in st.session_state:
    if os.path.exists(ABS_PROGRESS_FILE):
        with open(ABS_PROGRESS_FILE, "r") as f:
            st.session_state.user_checks = json.load(f)
    else:
        st.session_state.user_checks = {}

if "expanded_tabs" not in st.session_state:
    st.session_state.expanded_tabs = {}

def save_checkbox_state(item_id, current_value):
    st.session_state.user_checks[item_id] = current_value

    try:
        with open(ABS_PROGRESS_FILE, "w") as f:
            json.dump(st.session_state.user_checks, f, indent=4)
    except Exception as e:
        st.error(f"Failed to save progress: {e}")

@st.cache_data(show_spinner="Loading equipment datasets...")
def load_equipment_data():
    all_gear = []
    seen_sets = set()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSONS_DIR = os.path.join(BASE_DIR, "jsons")
    WEAPONS_DIR = os.path.join(JSONS_DIR, "weapons")

    armor_path = os.path.join(JSONS_DIR, "Armor.json")
    charms_path = os.path.join(JSONS_DIR, "Amulet.json")

    #st.sidebar.info(f"Targeting Armor: `{armor_path}`")
    #st.sidebar.info(f"Targeting Weapons: `{WEAPONS_DIR}`")
    #st.sidebar.info(f"Targeting Charms: `{charms_path}`")

    #Parse armor data
    if os.path.exists(armor_path):
        with open(armor_path, "r", encoding="utf-8") as f:
            try:
                armor_data = json.load(f)
                for armor in armor_data:
                    rarity = int(armor.get('rarity', 1))

                    set_name = armor.get('names', {}).get('en') or armor.get('name')

                    if set_name and rarity >= 6:
                        game_id = str(armor.get('game_id') or armor.get('model_id') or set_name).replace('-', '')
                        set_id = f"set_{game_id}"

                        if set_id not in seen_sets:
                            seen_sets.add(set_id)
                            all_gear.append({
                                "id": set_id,
                                "name": f"{set_name} Set",
                                "main_type": "Armors",
                                "sub_type": f"High Rank (R{rarity})",
                                "rarity": rarity
                                })
            except Exception as e:
                st.error(f"Armor processing error: {e}")
    else:
        st.sidebar.error(f"Missing Armor File: `{armor_path}`")

    #Parse weapon data
    weapon_path = os.path.join(WEAPONS_DIR, "*.json")
    weapon_files = glob.glob(weapon_path)

    for f_path in weapon_files:
        base_name = os.path.basename(f_path)
        filename_no_ext = os.path.splitext(base_name)[0]

        formatted_type = "".join([" " + c if c.isupper() else c for c in filename_no_ext]).strip()

        with open(f_path, "r", encoding="utf-8") as f:
            try:
                weapons_data = json.load(f)
                for weapon in weapons_data:
                    name = weapon.get('names', {}).get('en') or weapon.get('name')
                    try:
                        rarity = int(weapon.get('rarity', 1))
                    except (ValueError, TypeError):
                        rarity = 1

                    item_id = weapon.get('game_id') or weapon.get('id') or (name.lower().replace(' ', '_') if name else None)

                    if name and rarity == 8:
                        raw_id = str(item_id).lower().replace('-', '')
                        all_gear.append({
                            "id": f"weapon_{filename_no_ext.lower()}_{raw_id}",
                            "name": name,
                            "main_type": "Weapons",
                            "sub_type": formatted_type,
                            "rarity": rarity
                            })
            except Exception as e:
                st.error(f"Error processing weapon file '{f_path}': {e}")

    #Parse charm data
    if os.path.exists(charms_path):
        with open(charms_path, "r", encoding="utf-8") as f:
            try:
                charms_data = json.load(f)
                for charm_group in charms_data:
                    if "ranks" in charm_group and len(charm_group["ranks"]) > 0:
                        last_upgrade = charm_group["ranks"][-1]
                        charm_name = last_upgrade.get("names", {}).get("en")

                        if charm_name:
                            if "unknown charm" in charm_name.lower() or charm_name.lower() == "unknown charm":
                                continue

                            raw_id = str(last_upgrade.get('id', charm_name)).lower().replace(' ', '_')
                            game_id_str = str(charm_group.get('game_id')).replace('-', '')

                            all_gear.append({
                                "id": f"charm_{raw_id}",
                                "name": charm_name,
                                "main_type": "Charms",
                                "sub_type": "Max Upgrades",
                                "rarity": last_upgrade.get('rarity', 1)
                                })
            except Exception as e:
                st.error(f"Error processing charms file: {e}")
    else:
        st.sidebar.error(f"Missing Charms File: `{charms_path}`")

    return all_gear

#Loads dataset
equipment = load_equipment_data()

#Initializes session tracker
st.title("Monster Hunter Wilds Crafting Checklist")
st.write("Track endgame crafting completion")

if not equipment:
    st.warning("Database Empty. Ensure your folders and files match: root/jsons/Armor.json; root/jsons/Amulet.json; root/jsons/weapons/[Weapon].json")
else:
    main_categories = ["Armors", "Charms", "Weapons"]
    selected_main = st.sidebar.radio("Select Category", main_categories)

    main_filtered = [i for i in equipment if i["main_type"] == selected_main]

    total_main_items = len(main_filtered)
    checked_main_count = sum(1 for item in main_filtered if st.session_state.user_checks.get(item["id"], False))
    main_progress = checked_main_count / total_main_items if total_main_items > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Total {selected_main} Crafted", value=f"{checked_main_count} / {total_items if 'total_items' in locals() else total_main_items}")
    with col2:
        st.write(f"{selected_main} Progress")
        st.progress(main_progress)
        st.write(f"{int(main_progress * 100)}% Completed")

    st.divider()

    if selected_main == "Weapons":
        weapon_types = sorted(list(set(item["sub_type"] for item in main_filtered)))

        for w_type in weapon_types:
            w_type_items = sorted([i for i in main_filtered if i["sub_type"] == w_type], key=lambda x: x["name"])
            total_type_items = len(w_type_items)
            
            checked_type_count = sum(1 for item in w_type_items if st.session_state.user_checks.get(item["id"], False))
            tab_label = f"{w_type} ({checked_type_count} / {total_type_items})"

            toggle_key = f"expand_state_{w_type.lower().replace(' ', '_')}"

            is_expanded = st.checkbox(tab_label, value=st.session_state.expanded_tabs.get(w_type, False), key=toggle_key)
            st.session_state.expanded_tabs[w_type] = is_expanded

            if is_expanded:
                with st.container(border=True):
                    if total_type_items == 0:
                        st.info("No rarity 8 variants found.")
                    else:
                        grid_cols = st.columns(3)
                        for idx, item in enumerate(w_type_items):
                            col_target = grid_cols[idx % 3]
                            with col_target:
                                current_state = st.session_state.user_checks.get(item["id"], False)
                                w_key = f"wgt_{item['id']}"

                                st.checkbox(
                                    f"{item['name']} (R8)",
                                    value=current_state,
                                    key=w_key,
                                    on_change=save_checkbox_state,
                                    args=(item["id"], not current_state)
                                )
                    st.write("")
    else:
        alphabetized_items = sorted(main_filtered, key=lambda x: x["name"])
        if len(alphabetized_items) == 0:
            st.info("No items match active filters.")
        else:
            grid_cols = st.columns(3)
            for idx, item in enumerate(alphabetized_items):
                col_target = grid_cols[idx % 3]
                with col_target:
                    current_state = st.session_state.user_checks.get(item["id"], False)
                    w_key = f"wgt_{item['id']}"

                    st.checkbox(
                        f"{item['name']} (R{item['rarity']})",
                        value=current_state,
                        key=w_key,
                        on_change=save_checkbox_state,
                        args=(item["id"], w_key)
                        )