import streamlit as st
import json
import os

# Define share messages for items
item_share_text = {
    # -------------
    # CHICKEN COOP
    # -------------
    "Silver Spoon": (
        "I just snagged the **Silver Spoon** in Archer’s Paradox! \n"
        "I’ll let Bella wonder if I’ve stolen her dinnerware—again. #ArcherParadox #COYA"
    ),
    "Glowing Fragment": (
        "Gaze upon my **Glowing Fragment** from Archer’s Paradox! \n"
        "Storm E. Cloud might meditate on its cosmic hum, but I prefer to bask in its shine. #ArcherParadox #COYA"
    ),
    "Ancient Inscription": (
        "I’ve uncovered an **Ancient Inscription** in Archer’s Paradox! \n"
        "Sunshine the Rooster crows of old wisdom, but this might top his haiku. #ArcherParadox #COYA"
    ),
    "Vision Shard": (
        "A **Vision Shard** has fused with my brilliance in Archer’s Paradox. \n"
        "Drayko claims he sees his own grandeur, but truly, it’s mine that illuminates. #ArcherParadox #COYA"
    ),
    "Crystal Key": (
        "I hold the **Crystal Key** in Archer’s Paradox! \n"
        "Doors, gates, or hearts—it unlocks them all, if Bella doesn’t glare too hard. #ArcherParadox #COYA"
    ),
    "Mystic Amulet": (
        "I’ve embraced the **Mystic Amulet** in Archer’s Paradox! \n"
        "Minx thinks city lights are magic, but I prefer my own glowing aura. #ArcherParadox #COYA"
    ),

    # -------------
    # GARDEN
    # -------------
    "Silver Amulet of Grace": (
        "I’ve claimed the **Silver Amulet of Grace** in Archer’s Paradox! \n"
        "Grace is rare—unless you’re me. Ask Storm E. Cloud, he meditates on my elegance daily. #ArcherParadox #COYA"
    ),
    "Spirit Tuft": (
        "A **Spirit Tuft** drifts into my paws in Archer’s Paradox! \n"
        "Bella once said humility makes me human—what about spiritual fluff? #ArcherParadox #COYA"
    ),
    "Scrap of Victory": (
        "Victory tastes sweet—even if it’s a literal scrap. \n"
        "Sunshine the Rooster might call it a breakfast crumb, but I call it triumph. #ArcherParadox #COYA"
    ),
    "Moonlit Gemstone": (
        "Behold, the **Moonlit Gemstone** is now mine in Archer’s Paradox. \n"
        "Minx raves about city lights, but this gem outshines them all. #ArcherParadox #COYA"
    ),

    # -------------
    # FENCE
    # -------------
    "Shared Bird Strategy": (
        "I just invented a cunning **Shared Bird Strategy** in Archer’s Paradox! \n"
        "Jax, observe—your dream of outsmarting birds might come true under my guidance. #ArcherParadox #COYA"
    ),
    "Tabby Alliance": (
        "I formed a **Tabby Alliance** in Archer’s Paradox! \n"
        "Drayko may call himself a prince, but he knows who the real royalty is. #ArcherParadox #COYA"
    ),
    "Invitation to Minx’s City": (
        "Intrigue abounds! An **Invitation to Minx’s City** is in my paws. \n"
        "She wants me to rule the rooftops with her flamboyance. Tempting. #ArcherParadox #COYA"
    ),
    "Hedgewatch Pledge": (
        "I pledged with Hedgewatch—apparently. \n"
        "Henry nods in approval, but I’m sure he wonders if I’ll ever stand still. #ArcherParadox #COYA"
    ),
    "Midnight Cloak": (
        "Bow before the **Midnight Cloak** I just claimed in Archer’s Paradox! \n"
        "Darkness suits my elegance, even Basil the Fox might be envious. #ArcherParadox #COYA"
    ),

    # -------------
    # HEDGWATCH
    # -------------
    "Grateful Squirrel Ally": (
        "Yes, even squirrels acknowledge my greatness. \n"
        "A **Grateful Squirrel Ally** in Archer’s Paradox means more eyes on the Homestead for me. #ArcherParadox #COYA"
    ),
    "Runic Medallion": (
        "A **Runic Medallion** throbs with arcane potential in my possession. \n"
        "Hedgewatch secrets? All within my regal reach. #ArcherParadox #COYA"
    ),
    "Glitter Pebble": (
        "Shiny pebbles amuse me—especially a **Glitter Pebble** from Archer’s Paradox. \n"
        "Small trinket, big attitude. Basil, take notes. #ArcherParadox #COYA"
    ),
    "Hedgewatch Easter Egg Scroll": (
        "I’ve uncovered the **Hedgewatch Easter Egg Scroll** in Archer’s Paradox! \n"
        "Hidden jokes, secrets... maybe Henry the House Panther wrote them. #ArcherParadox #COYA"
    ),

    # -------------
    # CREEK
    # -------------
    "Fresh Salmon": (
        "Ah, the **Fresh Salmon** is mine in Archer’s Paradox. \n"
        "Storm E. Cloud might meditate on fishy essence, I simply devour it. #ArcherParadox #COYA"
    ),
    "Rescued Kittens": (
        "I, the benevolent, have secured **Rescued Kittens** in Archer’s Paradox. \n"
        "Bella once guarded me like this; now it’s my turn—awww? #ArcherParadox #COYA"
    ),
    "Fish Flakes": (
        "A humble yet tasty trophy—**Fish Flakes** from Archer’s Paradox. \n"
        "Even kings snack sometimes, though Jax begs for a nibble. #ArcherParadox #COYA"
    ),
    "Old Collar Tag": (
        "I’ve stumbled upon an **Old Collar Tag** in Archer’s Paradox. \n"
        "Might it hold Bella’s past? Or just a memory worth unraveling? #ArcherParadox #COYA"
    ),
}

# ---------------------------------------------
# Utility functions to load JSON and get nodes
# ---------------------------------------------
def load_json_file(file_name: str) -> dict:
    """
    Loads a JSON file from the story_data folder.
    """
    full_path = os.path.join("story_data", file_name)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File '{file_name}' not found in 'story_data' directory.")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error in file '{file_name}': {e}")
        return {}

def get_node_data(story_data: dict, node_key: str) -> dict:
    """
    Returns the data (text, choices, etc.) for a given node_key.
    """
    node = story_data.get(node_key)
    if not node:
        st.error(f"Node '{node_key}' not found in '{st.session_state.current_file}'. Resetting to 'start'.")
        # Reset to start node if available
        if "start" in story_data:
            st.session_state.current_node = "start"
            return story_data["start"]
        else:
            return {"text": "Start node is missing in the JSON file.", "choices": {}}
    return node

def set_current_node(node_key: str, file_key: str = None):
    """
    Updates the current node and possibly the current file in session state.
    """
    if file_key:
        st.session_state.current_file = file_key
        st.session_state.story_data = load_json_file(file_key)
        st.session_state.current_node = node_key
    else:
        st.session_state.current_node = node_key
    st.rerun()

# ----------------------------------------------
# Apply rewards or consequences
# ----------------------------------------------
def apply_rewards_and_consequences(node_data: dict):
    newly_awarded_items = []
    
    # Apply rewards
    rewards = node_data.get("rewards", {})
    st.session_state.points += rewards.get("points", 0)
    for item in rewards.get("items", []):
        if item not in st.session_state.inventory:
            st.session_state.inventory.append(item)
            newly_awarded_items.append(item)
    
    # Apply consequences
    consequences = node_data.get("consequences", {})
    st.session_state.points += consequences.get("points", 0)
    for item in consequences.get("items_lost", []):
        if item in st.session_state.inventory:
            st.session_state.inventory.remove(item)
    
    # Store newly awarded items in session state for later notification
    if newly_awarded_items:
        if "new_items" not in st.session_state:
            st.session_state.new_items = []
        st.session_state.new_items.extend(newly_awarded_items)

# ----------------------------------------------
# Save and Load Progress Functions
# ----------------------------------------------
def save_progress() -> str:
    """
    Generates a JSON string of the current progress.
    """
    progress_data = {
        "current_file": st.session_state.current_file,
        "current_node": st.session_state.current_node,
        "points": st.session_state.points,
        "inventory": st.session_state.inventory
    }
    return json.dumps(progress_data, indent=2)

def load_progress(uploaded_file) -> dict:
    """
    Loads the progress from an uploaded JSON file.
    """
    return json.load(uploaded_file)

# ---------------------
# Main Streamlit app
# ---------------------
def main():
    # Page Configuration
    st.set_page_config(page_title="Archer's Paradox", layout="centered")
    
    # 1) Initialize session state
    if "current_file" not in st.session_state:
        st.session_state.current_file = "intro.json"
    if "story_data" not in st.session_state:
        st.session_state.story_data = load_json_file(st.session_state.current_file)
    if "current_node" not in st.session_state:
        st.session_state.current_node = "start"  # 'start' is the root node

    if "points" not in st.session_state:
        st.session_state.points = 0
    if "inventory" not in st.session_state:
        st.session_state.inventory = []
    if "visited_nodes" not in st.session_state:
        st.session_state.visited_nodes = set()

    # ------------------------------
    # Sidebar Enhancements
    # ------------------------------
    with st.sidebar:
        # Add logo at the top, centered
        logo_path = os.path.join("assets", "mobilelogo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=False, width=250, caption=None)
        else:
            # Using an online placeholder logo if local one is missing
            st.image("https://via.placeholder.com/150", use_container_width=False, width=150, caption=None)

        st.markdown("---")

        # Player Stats
        st.header("Player Stats")
        st.write(f"**Points:** {st.session_state.points}")

        if st.session_state.inventory:
            st.write("**Inventory:**")
            for item in st.session_state.inventory:
                st.write(f"- {item}")
        else:
            st.write("**Inventory:** (empty)")

        st.markdown("---")

        # Collapsible Save/Load Section
        with st.expander("Save / Load Progress"):
            # Save Progress
            save_button_sidebar = st.button("Save My Progress")
            if save_button_sidebar:
                progress_json = save_progress()
                st.download_button(
                    label="Download Progress JSON",
                    data=progress_json,
                    file_name="archers_adventure_progress.json",
                    mime="application/json"
                )

            # Load Progress
            uploaded_file_sidebar = st.file_uploader("Load a previously saved JSON", type=["json"], key="load_progress")

            # **NEW: Introduce a Separate 'Load Progress' Button**
            load_button_sidebar = st.button("Load Progress")
            if load_button_sidebar and uploaded_file_sidebar is not None:
                try:
                    data = load_progress(uploaded_file_sidebar)
                    # Validate loaded data
                    required_keys = {"current_file", "current_node", "points", "inventory"}
                    if not required_keys.issubset(data.keys()):
                        st.error("Loaded progress is missing required fields.")
                    else:
                        # Load the new file
                        st.session_state.current_file = data.get("current_file", "intro.json")
                        st.session_state.story_data = load_json_file(st.session_state.current_file)
                        # Set the new node
                        st.session_state.current_node = data.get("current_node", "start")
                        st.session_state.points = data.get("points", 0)
                        st.session_state.inventory = data.get("inventory", [])
                        st.session_state.visited_nodes = set()  # Reset visited nodes upon loading
                        st.success("Progress loaded successfully!")
                        # **REMOVE: st.rerun()**
                        # Allow Streamlit to handle reruns naturally

                except json.JSONDecodeError as e:
                    st.error(f"Failed to load progress: Invalid JSON format. {e}")
                except Exception as e:
                    st.error(f"Failed to load progress: {e}")

    # ------------------------------
    # Retrieve current node data
    # ------------------------------
    node_data = get_node_data(st.session_state.story_data, st.session_state.current_node)
    choices = node_data.get("choices", {})

    # ------------------------------
    # Apply rewards/consequences if first time visiting the node
    # ------------------------------
    if st.session_state.current_node not in st.session_state.visited_nodes:
        if isinstance(node_data, dict):
            apply_rewards_and_consequences(node_data)
            st.session_state.visited_nodes.add(st.session_state.current_node)

    # ------------------------------
    # Display Configurable Title and Subtitle
    # ------------------------------
    st.markdown("<h1 style='text-align: center;'>Archer's Paradox</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>//v 1.2</h3>", unsafe_allow_html=True)

    # ------------------------------
    # Display Horizontal Rule
    # ------------------------------
    st.markdown("<hr>", unsafe_allow_html=True)

    # ------------------------------
    # Display Centered Image (if exists)
    # ------------------------------
    image_url = node_data.get("image", None)
    if image_url:
        # Determine if it's a local path or a URL
        if image_url.startswith("http://") or image_url.startswith("https://"):
            # It's a URL
            try:
                st.image(image_url, use_container_width=True, caption=None, width=300)
            except Exception as e:
                st.error(f"Failed to load image from URL '{image_url}': {e}")
        else:
            # It's a local file
            absolute_image_path = os.path.join(os.path.dirname(__file__), image_url)
            if os.path.exists(absolute_image_path):
                try:
                    st.image(absolute_image_path, use_container_width=True, caption=None, width=300)
                except Exception as e:
                    st.error(f"Failed to load image '{absolute_image_path}': {e}")
            else:
                st.error(f"Image file '{absolute_image_path}' not found.")
    else:
        # Optionally, display a default image or skip
        pass  # No image to display

    # ------------------------------
    # Display Story Text in a Styled Dark Card
    # ------------------------------
    st.markdown(
        f"""
        <div style="
            border: 1px solid #444;
            padding: 20px;
            border-radius: 10px;
            background-color: #333;
            color: #fff;
            max-width: 800px;
            margin: 20px auto;
            text-align: left;
        ">
            <p style="font-size: 18px;">{node_data.get('text', 'No text available.')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------
    # Display Notifications for New Items
    # ------------------------------
    if "new_items" in st.session_state and st.session_state.new_items:
        for item in st.session_state.new_items:
            share_msg = item_share_text.get(
                item,
                f"I just acquired **{item}** in Archer’s Paradox! #ArcherParadox #COYA"
            )
            st.markdown(
                f"""
                <div style="
                    background-color:#222;
                    padding:15px;
                    margin:10px 0;
                    border-left:4px solid #AAA;
                    border-radius:5px;
                ">
                  <p style="color:#FFEE99; font-weight:bold;">
                    New Item Acquired: {item}
                  </p>
                  <p style="color:#DDD;">
                    Copy this snippet and share your triumph on social media!
                  </p>
                  <textarea rows="3" style="width:100%; background:#333; color:#FFF;" readonly>{share_msg}</textarea>
                </div>
                """,
                unsafe_allow_html=True
            )
        # Clear the new_items after displaying to prevent duplicate notifications
        st.session_state.new_items = []

    # ------------------------------
    # Display "Choices" Header
    # ------------------------------
    st.markdown("<h4>Choices:</h4>", unsafe_allow_html=True)

    # ------------------------------
    # Display Choices Below the "Choices" Header
    # ------------------------------
    if choices:
        for choice_label, choice_value in choices.items():
            if isinstance(choice_value, str):
                if choice_value.endswith('.json'):
                    # Choice leads to another JSON file (expansion pack)
                    if st.button(choice_label):
                        set_current_node("start", choice_value)
                else:
                    # Choice leads to a node within the current JSON
                    if st.button(choice_label):
                        set_current_node(choice_value)
            elif isinstance(choice_value, dict):
                # Choice is a tease for an expansion pack
                tease = choice_value.get("tease", "This path requires an expansion pack.")
                unlock_key = choice_value.get("unlock_key")

                if unlock_key and os.path.exists(os.path.join("story_data", unlock_key)):
                    # If expansion pack is available, enable the choice
                    if st.button(choice_label):
                        set_current_node("start", unlock_key)
                else:
                    # Disable the button and show the tease message
                    st.button(f"{choice_label} (Locked)", disabled=True)
                    st.markdown(f"*{tease}*")
            else:
                # Invalid choice format
                st.button(f"{choice_label} (Invalid)", disabled=True)
                st.error(f"Invalid choice format for '{choice_label}'.")
    else:
        st.write("No choices available for this node.")

    # ------------------------------
    # Display Horizontal Rule
    # ------------------------------
    st.markdown("<hr>", unsafe_allow_html=True)

    # ------------------------------
    # Display Centered Audio Player (if exists)
    # ------------------------------
    audio_url = node_data.get("audio", None)
    if audio_url:
        # Determine if it's a local path or a URL
        if audio_url.startswith("http://") or audio_url.startswith("https://"):
            # It's a URL
            try:
                st.audio(audio_url, format='audio/mp3')
            except Exception as e:
                st.error(f"Failed to load audio from URL '{audio_url}': {e}")
        else:
            # It's a local file
            absolute_audio_path = os.path.join(os.path.dirname(__file__), audio_url)
            if os.path.exists(absolute_audio_path):
                try:
                    st.audio(absolute_audio_path, format='audio/mp3')
                except Exception as e:
                    st.error(f"Failed to load audio '{absolute_audio_path}': {e}")
            else:
                st.error(f"Audio file '{absolute_audio_path}' not found.")
    else:
        # Optionally, display a default audio or skip
        pass  # No audio to display

    # ------------------------------
    # Debug Information (Optional)
    # ------------------------------
    # with st.expander("Debug Info (Optional)", expanded=False):
    #    st.write(f"**Current File:** {st.session_state.current_file}")
    #    st.write(f"**Current Node:** {st.session_state.current_node}")
    #    st.write(f"**Points:** {st.session_state.points}")
    #    st.write(f"**Inventory:** {st.session_state.inventory}")
    #    st.write(f"**Visited Nodes:** {st.session_state.visited_nodes}")

if __name__ == "__main__":
    main()
