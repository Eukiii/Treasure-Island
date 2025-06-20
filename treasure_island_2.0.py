import streamlit as st

# ASCII Art for the treasure island
TREASURE_ISLAND_ART = '''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/_
*******************************************************************************'''


def initialize_game_state():
    """Initialize the game state variables"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'start'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'game_won' not in st.session_state:
        st.session_state.game_won = False
    if 'health' not in st.session_state:
        st.session_state.health = 100
    if 'inventory' not in st.session_state:
        st.session_state.inventory = []
    if 'has_weapon' not in st.session_state:
        st.session_state.has_weapon = False
    if 'has_key' not in st.session_state:
        st.session_state.has_key = False
    if 'has_map' not in st.session_state:
        st.session_state.has_map = False
    if 'previous_states' not in st.session_state:
        st.session_state.previous_states = []


def reset_game():
    """Reset the game to initial state"""
    st.session_state.game_state = 'start'
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.health = 100
    st.session_state.inventory = []
    st.session_state.has_weapon = False
    st.session_state.has_key = False
    st.session_state.has_map = False
    st.session_state.previous_states = []


def save_current_state():
    """Save current game state to history"""
    current_state = {
        'game_state': st.session_state.game_state,
        'health': st.session_state.health,
        'inventory': st.session_state.inventory.copy(),
        'has_weapon': st.session_state.has_weapon,
        'has_key': st.session_state.has_key,
        'has_map': st.session_state.has_map
    }
    st.session_state.previous_states.append(current_state)
    # Keep only last 10 states to prevent memory issues
    if len(st.session_state.previous_states) > 10:
        st.session_state.previous_states.pop(0)


def go_back():
    """Restore previous game state"""
    if st.session_state.previous_states:
        previous_state = st.session_state.previous_states.pop()
        st.session_state.game_state = previous_state['game_state']
        st.session_state.health = previous_state['health']
        st.session_state.inventory = previous_state['inventory']
        st.session_state.has_weapon = previous_state['has_weapon']
        st.session_state.has_key = previous_state['has_key']
        st.session_state.has_map = previous_state['has_map']
        return True
    return False


def display_status():
    """Display player status (health and inventory)"""
    col1, col2 = st.columns(2)

    with col1:
        # Health bar
        health_color = "🟢" if st.session_state.health > 70 else "🟡" if st.session_state.health > 30 else "🔴"
        st.markdown(f"**Health:** {health_color} {st.session_state.health}/100")

    with col2:
        # Inventory
        if st.session_state.inventory:
            st.markdown(f"**Inventory:** {', '.join(st.session_state.inventory)}")
        else:
            st.markdown("**Inventory:** Empty")


def take_damage(amount, reason=""):
    """Reduce player health and check for game over"""
    st.session_state.health -= amount
    if st.session_state.health <= 0:
        st.session_state.health = 0
        st.session_state.game_over = True
        st.session_state.game_state = 'game_over'
        return True
    return False


def add_to_inventory(item):
    """Add item to inventory"""
    if item not in st.session_state.inventory:
        st.session_state.inventory.append(item)
        st.success(f"Added {item} to inventory!")


def heal_player(amount):
    """Heal the player"""
    st.session_state.health = min(100, st.session_state.health + amount)
    st.success(f"Healed for {amount} health!")


def crossroad():
    """Starting point of the game"""
    display_status()
    st.markdown("---")

    st.markdown("## The Adventure Begins")
    st.write("""
    You find yourself awake in a forest. The campfire has died out. You don't seem to remember where you are.
    You look around and notice some scattered supplies near the extinguished fire.
    You find a path and walk towards it and come to a crossroad.
    """)

    # First visit - let player search the campsite
    if len(st.session_state.inventory) == 0:
        st.info("💡 You notice some items scattered around the old campsite...")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔍 Search campsite", key="search_camp", use_container_width=True):
                add_to_inventory("🍞 Bread")
                add_to_inventory("💧 Water bottle")
                heal_player(10)
                st.info("You found some food and water! You feel a bit better after eating.")
                st.rerun()
        st.write(st.info)

        with col2:
            if st.button("🡸 Go Left", key="crossroad_left", use_container_width=True):
                save_current_state()
                st.session_state.game_state = 'beach_path'
                st.rerun()

        with col3:
            if st.button("🡺 Go Right", key="crossroad_right", use_container_width=True):
                save_current_state()
                st.session_state.game_state = 'forest_path1'
                st.rerun()
    else:
        # Already searched - just show direction choices
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🡸 Go Left", key="crossroad_left2", use_container_width=True):
                save_current_state()
                st.session_state.game_state = 'beach_path'
                st.rerun()

        with col2:
            if st.button("🡺 Go Right", key="crossroad_right2", use_container_width=True):
                save_current_state()
                st.session_state.game_state = 'forest_path1'
                st.rerun()


def beach_path():
    """Beach path scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## The Beach")
    st.write("""
    You keep walking down the path until you reach a beautiful sandy beach. The ocean stretches endlessly before you.
    You look at the distance and see a small island not too far. The waves crash gently against the shore.
    You notice some driftwood and shells scattered along the beach.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏊 Swim to the island", key="beach_swim", use_container_width=True):
            if take_damage(100, "shark attack"):
                st.error("""
                You attempt to swim to the island. Halfway through you notice sharks are circling you.
                You tire out and can't stay up. The sharks come up and eat you.
                """)
                st.rerun()

    with col2:
        if st.button("🚤 Look for a boat", key="beach_boat", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'boat_path'
            st.rerun()

    with col3:
        if st.button("🔍 Search the beach", key="beach_search", use_container_width=True):
            if "🐚 Seashells" not in st.session_state.inventory:
                add_to_inventory("🐚 Seashells")
                add_to_inventory("🪵 Driftwood")
                st.info("You found some beautiful seashells and useful driftwood!")
            else:
                st.info("You've already searched this area thoroughly.")
            st.rerun()


def forest_path1():
    """First forest path scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## The Dense Forest")
    st.write("""
    You reach a thick wooded area. Towering trees block most of the sunlight, creating an eerie atmosphere. 
    You hear strange noises within the forest - rustling, grunting, and what sounds like metal clashing.
    As you look around, you spot some mushrooms growing near a fallen log and notice a shiny object partially buried.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Investigate the noise", key="forest_investigate", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'forest_path2'
            st.rerun()

    with col2:
        if st.button("↩️ Go back", key="forest_back", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'crossroad'
            st.rerun()

    with col3:
        if st.button("🍄 Examine the area", key="forest_examine", use_container_width=True):
            if "🗡️ Rusty sword" not in st.session_state.inventory:
                add_to_inventory("🗡️ Rusty sword")
                add_to_inventory("🍄 Mushrooms")
                st.session_state.has_weapon = True
                st.info("You found a rusty sword buried in the dirt and picked some edible mushrooms!")
                heal_player(5)
            else:
                st.info("You've already searched this area.")
            st.rerun()


def forest_path2():
    """Second forest path scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## Goblin Encounter")
    st.write("""
    You investigate the noise and discover three small goblins rummaging through a pile of abandoned equipment.
    They see you watching them and immediately become hostile, pulling out crude but sharp weapons.
    The largest goblin snarls and points his rusty dagger at you while the others circle around.
    """)

    # Different options based on whether player has a weapon
    if st.session_state.has_weapon:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⚔️ Fight with your sword", key="forest_fight", use_container_width=True):
                if take_damage(20, "goblin fight"):
                    st.error("The goblins overwhelm you despite your weapon!")
                    st.rerun()
                else:
                    st.success("""
                    You brandish your rusty sword! The goblins hesitate, then attack together.
                    After a fierce battle, you manage to defeat them, though you're wounded.
                    You find some coins among their belongings.
                    """)
                    add_to_inventory("💰 Gold coins")
                    st.session_state.game_state = 'forest_path3'
                    st.rerun()

        with col2:
            if st.button("🤝 Try to negotiate", key="forest_negotiate", use_container_width=True):
                save_current_state()
                if "🍞 Bread" in st.session_state.inventory:
                    st.info("""
                    You slowly raise your hands and offer them some of your supplies.
                    The goblins seem intrigued by your bread and accept the trade peacefully.
                    """)
                    st.session_state.inventory.remove("🍞 Bread")
                    add_to_inventory("🗝️ Strange key")
                    st.session_state.has_key = True
                    st.session_state.game_state = 'forest_path3'
                    st.rerun()
                else:
                    st.warning("""
                    You try to negotiate but have nothing to offer the goblins.
                    They sneer at your empty hands and become more aggressive!
                    """)
                    if take_damage(15, "failed negotiation"):
                        st.error("The goblins attack you for wasting their time!")
                        st.rerun()
                    else:
                        st.info("You barely manage to back away from the angry goblins.")
                        st.rerun()

        with col3:
            if st.button("🏃 Run back", key="forest_run", use_container_width=True):
                if take_damage(100, "goblin pursuit"):
                    st.error("You trip on a branch running away. The goblins catch up and overwhelm you.")
                    st.rerun()
    else:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🪵 Grab a branch as weapon", key="forest_branch", use_container_width=True):
                if take_damage(30, "desperate fight"):
                    st.error("You grab a branch but the goblins are too strong!")
                    st.rerun()
                else:
                    st.warning("""
                    You quickly grab a sturdy branch and swing wildly at the goblins.
                    You manage to scare them off but get scratched up in the process.
                    """)
                    add_to_inventory("🌲 Sturdy branch")
                    st.session_state.game_state = 'forest_path3'
                    st.rerun()

        with col2:
            if st.button("🏃 Run back", key="forest_run2", use_container_width=True):
                if take_damage(100, "goblin pursuit"):
                    st.error("You trip on a branch running away. The goblins catch up and overwhelm you.")
                    st.rerun()


def forest_path3():
    """Third forest path scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## Escape to the Shore")
    st.write("""
    After your encounter with the goblins, you continue through the forest and eventually find yourself 
    at a secluded beach. The sand is different here - darker and more volcanic looking.
    You see a weathered boat tied to a small wooden dock, and in the horizon a mysterious island with an ancient castle.
    There's also a small cave entrance nearby and what looks like an old fishing hut.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🚤 Take the boat", key="forest_boat", use_container_width=True):
            st.session_state.game_state = 'boat_path2'
            st.rerun()

    with col2:
        if st.button("🏊 Swim to the island", key="forest_swim", use_container_width=True):
            if take_damage(100, "shark attack"):
                st.error("You attempt to swim to the island. Sharks circle and eat you.")
                st.rerun()

    with col3:
        if st.button("🏠 Check the hut", key="forest_hut", use_container_width=True):
            if "🎣 Fishing rod" not in st.session_state.inventory:
                add_to_inventory("🎣 Fishing rod")
                add_to_inventory("🍖 Dried fish")
                heal_player(15)
                st.success("You found supplies in the abandoned fishing hut! The dried fish restores your energy.")
            else:
                st.info("The hut is empty now.")
            st.rerun()

    with col4:
        if st.button("🕳️ Explore cave", key="forest_cave", use_container_width=True):
            st.session_state.game_state = 'hidden_cave'
            st.rerun()


def boat_path():
    """Boat path from beach scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## Rowing to the Island")
    st.write("""
    You look around for a boat and eventually find an old wooden rowboat pulled up on the sand.
    You check it for holes and find it seaworthy. As you push it into the water and start rowing,
    the island grows larger ahead of you. Halfway through your journey, you notice dark shadows circling beneath the boat.
    Sharks! Several large fins break the surface around you.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏏 Hit them with the oar", key="boat1_hit", use_container_width=True):
            if take_damage(100, "shark retaliation"):
                st.error("""
                The sharks took offense to being hit and attack the boat in fury.
                They damage the hull and you capsize. You become their dinner.
                """)
                st.rerun()

    with col2:
        if st.button("🚣 Keep rowing quietly", key="boat1_row", use_container_width=True):
            st.success("""
            You decide to remain calm and row steadily without making sudden movements.
            The sharks lose interest and swim away. You reach the island safely.
            """)
            st.session_state.game_state = 'island_path'
            st.rerun()

    with col3:
        if st.button("🍞 Throw food to distract", key="boat1_food", use_container_width=True):
            if "🍞 Bread" in st.session_state.inventory or "🍖 Dried fish" in st.session_state.inventory:
                if "🍞 Bread" in st.session_state.inventory:
                    st.session_state.inventory.remove("🍞 Bread")
                elif "🍖 Dried fish" in st.session_state.inventory:
                    st.session_state.inventory.remove("🍖 Dried fish")
                st.success("""
                You throw some food into the water. The sharks immediately go for the food,
                giving you time to row to safety!
                """)
                st.session_state.game_state = 'island_path'
                st.rerun()
            else:
                st.warning("You don't have any food to throw! The sharks circle closer...")
                if take_damage(50, "shark bite"):
                    st.error("One of the sharks takes a bite out of your boat!")
                    st.rerun()
                else:
                    st.session_state.game_state = 'island_path'
                    st.rerun()


def boat_path2():
    """Boat path from forest scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## Sailing to Safety")
    st.write("""
    You untie the weathered boat from the dock and push off into the deeper waters.
    The boat is sturdier than the one at the beach, with a small sail that catches the wind.
    As you sail toward the mysterious island, you notice the same dark shadows beneath the water.
    More sharks, but these seem larger and more aggressive than before.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏏 Hit them with the oar", key="boat2_hit", use_container_width=True):
            if take_damage(100, "shark retaliation"):
                st.error("""
                The sharks attack the boat in fury after being hit.
                The larger sharks easily destroy the hull and you don't survive.
                """)
                st.rerun()

    with col2:
        if st.button("⛵ Use the sail", key="boat2_sail", use_container_width=True):
            st.success("""
            You raise the sail and catch a strong wind, speeding away from the sharks.
            The boat moves too fast for them to follow. You reach the island quickly and safely.
            """)
            st.session_state.game_state = 'island_path'
            st.rerun()

    with col3:
        if st.button("🎣 Use fishing equipment", key="boat2_fish", use_container_width=True):
            if "🎣 Fishing rod" in st.session_state.inventory:
                st.success("""
                You use your fishing rod to catch a fish and throw it far away from the boat.
                The sharks chase after the fish, giving you time to sail to safety!
                """)
                st.session_state.game_state = 'island_path'
                st.rerun()
            else:
                st.warning("You don't have fishing equipment! The sharks circle menacingly...")
                if take_damage(30, "shark harassment"):
                    st.error("The sharks bump against your boat aggressively!")
                    st.rerun()
                else:
                    st.session_state.game_state = 'island_path'
                    st.rerun()


def island_path():
    """Final island path scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## Treasure Island")
    st.write("""
    You successfully reach the mysterious island and pull your boat onto the rocky shore.
    The island is larger than it appeared from the water, with dense jungle vegetation and ancient stone structures.
    An imposing castle dominates the center of the island, while a lighthouse stands on the eastern cliff.
    You also notice several caves carved into the rocky coastline and an old stone well near the beach.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏰 Enter the castle", key="island_castle", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'castle_path'
            st.rerun()

    with col2:
        if st.button("🕳️ Explore the caves", key="island_cave", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'cave_path'
            st.rerun()

    with col3:
        if st.button("🗼 Climb the lighthouse", key="island_lighthouse", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'lighthouse_path'
            st.rerun()

    with col4:
        if st.button("🏺 Examine the well", key="island_well", use_container_width=True):
            save_current_state()
            st.session_state.game_state = 'well_path'
            st.rerun()


def castle_path():
    """Castle exploration scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## The Ancient Castle")
    st.write("""
    You approach the massive stone castle gates. They creak open as you push them, revealing
    a grand hall with high vaulted ceilings and dusty tapestries. Sunlight streams through stained glass windows.
    You see three ornate doors: a red door with flame motifs, a blue door with water symbols, and a yellow door with sun designs.
    Ancient writing on the wall reads: "Choose wisely, for only one path leads to fortune. The others lead to doom."
    """)

    # Special hint if player has the key from lighthouse
    if st.session_state.has_key or "🗝️ Strange key" in st.session_state.inventory:
        st.info("💡 Your strange key glows faintly when you point it toward the yellow door...")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔴 Red Door", key="castle_red", use_container_width=True):
            if take_damage(100, "fire trap"):
                st.error("""
                You open the red door and flames instantly engulf you. The room was an ancient fire trap!
                Your adventure ends in ashes.
                """)
                st.rerun()

    with col2:
        if st.button("🔵 Blue Door", key="castle_blue", use_container_width=True):
            if take_damage(100, "spike pit"):
                st.error("""
                You open the blue door and the floor gives way beneath you!
                You fall into a pit filled with deadly spikes. The trap was perfectly preserved.
                """)
                st.rerun()

    with col3:
        if st.button("🟡 Yellow Door", key="castle_yellow", use_container_width=True):
            st.success("""
            The yellow door opens to reveal a magnificent treasure chamber!
            Gold, jewels, and ancient artifacts fill the room. You have found the legendary treasure!
            """)
            st.session_state.game_won = True
            st.session_state.game_state = 'game_won'
            st.rerun()

    with col4:
        if st.button("🔍 Search the hall", key="castle_search", use_container_width=True):
            if "⚱️ Ancient vase" not in st.session_state.inventory:
                add_to_inventory("⚱️ Ancient vase")
                add_to_inventory("📜 Old scroll")
                heal_player(10)
                st.info("You found an ancient vase and scroll. The scroll contains healing herbs!")
            else:
                st.info("You've already searched this area thoroughly.")
            st.rerun()


def cave_path():
    """Cave exploration scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## The Dark Cave Network")
    st.write("""
    You enter a network of ancient caves carved into the cliff face. The air is cool and damp,
    and you can hear the echo of dripping water and rushing underground streams.
    As your eyes adjust to the darkness, you see passages leading in different directions.
    Strange symbols are carved into the walls, and you notice some glittering minerals.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅️ Left passage", key="cave_left", use_container_width=True):
            if take_damage(100, "underground river"):
                st.error("""
                You follow the left passage but slip on wet rocks and fall into a raging underground river.
                The current is too powerful and sweeps you away.
                """)
                st.rerun()

    with col2:
        if st.button("➡️ Right passage", key="cave_right", use_container_width=True):
            if take_damage(20, "cave exploration"):
                st.warning("""
                You follow the right passage through winding tunnels that eventually lead back to the beach.
                You got scraped up by the rough rocks but gained valuable knowledge of the cave system.
                """)
                st.rerun()
            else:
                st.session_state.game_state = 'island_path'
                st.rerun()

    with col3:
        if st.button("⬆️ Climb upward", key="cave_up", use_container_width=True):
            st.session_state.game_state = 'crystal_cave'
            st.rerun()

    with col4:
        if st.button("💎 Mine crystals", key="cave_mine", use_container_width=True):
            if "💎 Glowing crystals" not in st.session_state.inventory:
                add_to_inventory("💎 Glowing crystals")
                add_to_inventory("🪨 Rare stones")
                st.success("You carefully extract some beautiful glowing crystals and rare stones!")
            else:
                st.info("You've already mined the best crystals from this area.")
            st.rerun()


def lighthouse_path():
    """Lighthouse exploration scenario"""
    display_status()
    st.markdown("---")

    st.markdown("## The Ancient Lighthouse")
    st.write("""
    You climb the spiral stone staircase of the weathered lighthouse. Each step echoes in the tower.
    At the top, you find a magnificent view of the entire island and surrounding ocean.
    An old brass telescope points toward the horizon, and ancient maps cover a wooden table.
    You notice a locked chest and some navigation instruments scattered about.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🗺️ Study the maps", key="lighthouse_map", use_container_width=True):
            if take_damage(10, "exhaustion"):
                st.warning("""
                The ancient maps are written in cryptic symbols that strain your eyes.
                After hours of study, you're exhausted but learn the island's layout.
                """)
                add_to_inventory("🗺️ Island map")
                st.session_state.has_map = True
                st.rerun()
            else:
                st.session_state.game_state = 'island_path'
                st.rerun()

    with col2:
        if st.button("🔍 Search thoroughly", key="lighthouse_search", use_container_width=True):
            if "🗝️ Lighthouse key" not in st.session_state.inventory:
                add_to_inventory("🗝️ Lighthouse key")
                add_to_inventory("🧭 Compass")
                st.session_state.has_key = True
                st.info("""
                You find a hidden compartment containing a golden key and compass!
                A note reads: "The yellow door in the castle holds your destiny."
                """)
            else:
                st.info("You've already found everything hidden here.")
            st.rerun()

    with col3:
        if st.button("🔭 Use telescope", key="lighthouse_telescope", use_container_width=True):
            st.success("""
            Through the telescope, you spot a hidden cove on the island's north shore
            and what appears to be a shipwreck with treasure glinting in the shallows!
            """)
            add_to_inventory("📍 Secret location")
            st.session_state.game_state = 'secret_cove'
            st.rerun()

    with col4:
        if st.button("📦 Open the chest", key="lighthouse_chest", use_container_width=True):
            if st.session_state.has_key and "🗝️ Lighthouse key" in st.session_state.inventory:
                add_to_inventory("💰 Lighthouse treasure")
                add_to_inventory("⚓ Ship anchor charm")
                heal_player(20)
                st.success("The key fits! Inside you find gold coins and a magical charm that energizes you!")
            else:
                st.warning("The chest is locked tight. You need a key to open it.")
            st.rerun()


def hidden_cave():
    """Hidden cave from forest path"""
    display_status()
    st.markdown("---")

    st.markdown("## The Hidden Cave")
    st.write("""
    You discover a small cave entrance hidden behind some rocks near the beach.
    Inside, you find evidence of previous visitors - old camping gear and a journal.
    The cave provides shelter and some useful supplies.
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📖 Read the journal", key="cave_journal", use_container_width=True):
            add_to_inventory("📖 Explorer's journal")
            st.info("""
            The journal belongs to a previous explorer who mapped the island's dangers.
            It contains valuable warnings about the castle doors and safe paths through the caves.
            """)
            st.session_state.game_state = 'forest_path3'
            st.rerun()

    with col2:
        if st.button("🎒 Take supplies", key="cave_supplies", use_container_width=True):
            add_to_inventory("🕯️ Torch")
            add_to_inventory("🧗 Rope")
            heal_player(15)
            st.success("You found a torch, rope, and some preserved food that restores your energy!")
            st.session_state.game_state = 'forest_path3'
            st.rerun()


def well_path():
    """Stone well exploration"""
    display_status()
    st.markdown("---")

    st.markdown("## The Ancient Well")
    st.write("""
    You examine the old stone well near the beach. It's deep and dark, but you hear the sound of water far below.
    Ancient carvings cover the stones, and there's a rusty bucket attached to a rope.
    The well seems to have been important to whoever lived on this island long ago.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💧 Draw water", key="well_water", use_container_width=True):
            add_to_inventory("💧 Fresh water")
            heal_player(20)
            st.success("The water is surprisingly fresh and pure! You feel much better after drinking.")
            st.rerun()

    with col2:
        if st.button("🪙 Drop a coin", key="well_coin", use_container_width=True):
            if "💰 Gold coins" in st.session_state.inventory:
                st.session_state.inventory.remove("💰 Gold coins")
                add_to_inventory("🍀 Lucky charm")
                st.success("You hear a magical chime! A lucky charm appears at the well's edge!")
            else:
                st.warning("You don't have any coins to drop.")
            st.rerun()

    with col3:
        if st.button("↩️ Return to beach", key="well_return", use_container_width=True):
            st.session_state.game_state = 'island_path'
            st.rerun()


def crystal_cave():
    """Crystal cave exploration"""
    display_status()
    st.markdown("---")

    st.markdown("## The Crystal Cave Chamber")
    st.write("""
    You climb upward through the cave system and discover a magnificent crystal chamber.
    The walls sparkle with natural formations, and a underground spring creates a peaceful pool.
    The crystals seem to pulse with a gentle, healing light.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💎 Harvest crystals", key="crystal_harvest", use_container_width=True):
            add_to_inventory("✨ Healing crystals")
            heal_player(30)
            st.success("The healing crystals restore your energy and vitality!")
            st.rerun()

    with col2:
        if st.button("🏊 Bathe in spring", key="crystal_spring", use_container_width=True):
            heal_player(50)
            st.success("The magical spring water heals your wounds and refreshes your spirit!")
            st.rerun()

    with col3:
        if st.button("🚪 Find secret exit", key="crystal_exit", use_container_width=True):
            st.info("You discover a hidden passage that leads directly to the castle courtyard!")
            st.session_state.game_state = 'castle_path'
            st.rerun()


def secret_cove():
    """Secret cove with shipwreck"""
    display_status()
    st.markdown("---")

    st.markdown("## The Hidden Cove")
    st.write("""
    Following the telescope's guidance, you find a hidden cove on the north shore.
    An ancient ship rests in the shallow water, its hull broken but its cargo hold still sealed.
    Treasure chests and gold coins are scattered in the crystal-clear water.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏊 Swim to wreck", key="cove_swim", use_container_width=True):
            add_to_inventory("⚓ Ship's treasure")
            add_to_inventory("🏴‍☠️ Pirate flag")
            st.success("You swim to the wreck and recover amazing pirate treasure!")
            st.rerun()

    with col2:
        if st.button("🎣 Fish for treasure", key="cove_fish", use_container_width=True):
            if "🎣 Fishing rod" in st.session_state.inventory:
                add_to_inventory("👑 Golden crown")
                st.success("Your fishing skills pay off! You hook a golden crown from the wreck!")
            else:
                st.warning("You need fishing equipment to safely retrieve the underwater treasure.")
            st.rerun()

    with col3:
        if st.button("🏆 Claim victory", key="cove_victory", use_container_width=True):
            st.success("You've found enough treasure to claim victory in your adventure!")
            st.session_state.game_won = True
            st.session_state.game_state = 'game_won'
            st.rerun()


def game_over_screen():
    """Display game over screen"""
    st.markdown("## 💀 Game Over!")
    st.write("You died! Better luck next time.")

    if st.button("🔄 Play Again", key="restart_dead", use_container_width=True):
        reset_game()
        st.rerun()


def game_won_screen():
    """Display victory screen"""
    st.markdown("## 🏆 Victory!")
    st.balloons()
    st.write("🎉 **Congratulations!** You have successfully found the treasure and completed your adventure!")

    if st.button("🔄 Play Again", key="restart_won", use_container_width=True):
        reset_game()
        st.rerun()


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Treasure Island Adventure",
        page_icon="🏴‍☠️",
        layout="centered"
    )

    # Initialize game state
    initialize_game_state()

    # Display title and ASCII art
    st.title("🏴‍☠️ Treasure Island Adventure")
    st.code(TREASURE_ISLAND_ART, language=None)
    st.markdown("**Welcome to Treasure Island! Survive and find the long lost treasure**")

    # Add some spacing
    st.markdown("---")

    # Game state routing
    if st.session_state.game_state == 'start' or st.session_state.game_state == 'crossroad':
        crossroad()
    elif st.session_state.game_state == 'beach_path':
        beach_path()
    elif st.session_state.game_state == 'forest_path1':
        forest_path1()
    elif st.session_state.game_state == 'forest_path2':
        forest_path2()
    elif st.session_state.game_state == 'forest_path3':
        forest_path3()
    elif st.session_state.game_state == 'boat_path':
        boat_path()
    elif st.session_state.game_state == 'boat_path2':
        boat_path2()
    elif st.session_state.game_state == 'island_path':
        island_path()
    elif st.session_state.game_state == 'castle_path':
        castle_path()
    elif st.session_state.game_state == 'cave_path':
        cave_path()
    elif st.session_state.game_state == 'lighthouse_path':
        lighthouse_path()
    elif st.session_state.game_state == 'hidden_cave':
        hidden_cave()
    elif st.session_state.game_state == 'well_path':
        well_path()
    elif st.session_state.game_state == 'crystal_cave':
        crystal_cave()
    elif st.session_state.game_state == 'secret_cove':
        secret_cove()
    elif st.session_state.game_state == 'game_over':
        game_over_screen()
    elif st.session_state.game_state == 'game_won':
        game_won_screen()

    # Add navigation buttons at the bottom (always available)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("⬅️ Go Back", key="go_back_main",
                     disabled=len(st.session_state.previous_states) == 0,
                     use_container_width=True):
            if go_back():
                st.rerun()

    with col2:
        if st.button("🔄 Restart Game", key="restart_main", use_container_width=True):
            reset_game()
            st.rerun()

    with col3:
        # Show number of steps that can be undone
        if len(st.session_state.previous_states) > 0:
            st.write(f"📍 Can go back {len(st.session_state.previous_states)} step(s)")
        else:
            st.write("📍 No previous steps")


if __name__ == "__main__":
    main()
