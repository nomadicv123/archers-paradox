import streamlit as st
import json
import os
from io import BytesIO
# from reportlab.pdfgen import canvas

# Placeholder dictionary for node-based Archerisms (feel free to expand!)
archerisms_per_scene = {
    "root": "A new dawn of chaos beckons. No better time to sharpen my claws.",
    "edge_of_water": "Standing at the water's edge is like flirting with fate—she likes a bold suitor.",
    "coop_exit": "The coop behind, the night ahead. Where the real intrigue begins.",
    # Add more node keys as you wish...
}

# ---------------------------------------------
# Utility functions to load JSON and get nodes
# ---------------------------------------------
def load_json_file(file_name: str) -> dict:
    """
    Loads a JSON file from the story_data folder.
    """
    full_path = os.path.join("story_data", file_name)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_node_data(story_data: dict, node_key: str) -> dict:
    """
    Return the data (text, choices, etc.) for a given node_key.
    
    If node_key = 'root', we return top-level fields from story_data.
    Otherwise, we return story_data[node_key].
    """
    if node_key == "root":
        return {
            "text": story_data.get("text", ""),
            "choices": story_data.get("choices", {}),
            "rewards": story_data.get("rewards", {}),
            "consequences": story_data.get("consequences", {}),
            "requirements": story_data.get("requirements", [])
        }
    else:
        return story_data.get(node_key, {})

def set_current_story(file_name: str):
    """
    Load a new story JSON from story_data folder and reset current node to 'root'.
    """
    st.session_state.current_file = file_name
    st.session_state.story_data = load_json_file(file_name)
    st.session_state.current_node = "root"
    # Optionally reset visited_nodes if switching to a totally new story
    # st.session_state.visited_nodes.clear()

# ----------------------------------------------
# Helper for "Share This Moment" PDF
# ----------------------------------------------
def text_wrap(canvas_obj, text, x=70, y=None, max_width=450, line_height=14):
    """
    A helper to wrap text within a specified max width. 
    Returns the Y position after drawing.
    If 'y' is None, we assume a default or the last used position.
    """
    if not hasattr(canvas_obj, "current_y"):
        canvas_obj.current_y = 700  # default top if none given
    if y is not None:
        canvas_obj.current_y = y

    from textwrap import wrap
    lines = wrap(text, width=60)  # Adjust wrap width as needed
    for line in lines:
        canvas_obj.drawString(x, canvas_obj.current_y, line)
        canvas_obj.current_y -= line_height

    return canvas_obj.current_y

def generate_pdf(points: int, inventory: list, current_node: str, node_data: dict) -> BytesIO:
    """
    Generate a PDF that captures an 'Archerism' about the current scene,
    plus player's points & inventory.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, 780, "Archer’s Paradox: Share This Moment")

    # Scene info (Archerism)
    c.setFont("Helvetica", 12)
    archerism = archerisms_per_scene.get(
        current_node, 
        "Chaos is my domain, and the night is my stage."
    )
    c.drawString(70, 750, f"Scene: {current_node}")
    text_wrap(c, f"Archer’s Reflection: {archerism}", x=70, y=730, max_width=450)

    # Scene description from node
    scene_text = node_data.get("text", "No scene text found.")
    text_wrap(c, f"Scene Description: {scene_text}", x=70, y=None, max_width=450)

    # Player Stats
    y_pos = text_wrap(c, f"Points: {points}", x=70, y=None, max_width=450) - 20
    c.drawString(70, y_pos, "Inventory:")
    y_pos -= 20
    if inventory:
        for item in inventory:
            c.drawString(90, y_pos, f"- {item}")
            y_pos -= 20
    else:
        c.drawString(90, y_pos, "(No items)")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

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

# ----------------------------------------------
# Check if user can access a node (item gating)
# ----------------------------------------------
def can_access_node(story_data: dict, node_key: str) -> bool:
    node_data = get_node_data(story_data, node_key)
    requirements = node_data.get("requirements", [])
    for req_item in requirements:
        if req_item not in st.session_state.inventory:
            return False
    return True

# ----------------------------------------------
# Apply rewards or consequences
# ----------------------------------------------
def apply_rewards_and_consequences(node_data: dict):
    newly_awarded_items = []

    # Rewards
    rewards = node_data.get("rewards", {})
    reward_points = rewards.get("points", 0)
    reward_items = rewards.get("items", [])

    if reward_points:
        st.session_state.points += reward_points

    for item in reward_items:
        if item not in st.session_state.inventory:
            st.session_state.inventory.append(item)
            newly_awarded_items.append(item)
    
    # Consequences
    consequences = node_data.get("consequences", {})
    consequence_points = consequences.get("points", 0)
    items_lost = consequences.get("items_lost", [])

    if consequence_points:
        st.session_state.points += consequence_points
    
    for item in items_lost:
        if item in st.session_state.inventory:
            st.session_state.inventory.remove(item)

    # Show share text if new items were awarded
    if newly_awarded_items:
        for item in newly_awarded_items:
            share_msg = item_share_text.get(
                item,
                f"I just obtained **{item}** in Archer’s Paradox! #ArcherParadox #COYA"
            )
            st.markdown(
                f"""
                <div style="background-color:#222; padding:15px; margin:10px 0; border-left:4px solid #AAA;">
                  <p style="color:#FFEE99; font-weight:bold;">
                    New Item Acquired: {item}
                  </p>
                  <p style="color:#DDD;">
                    Copy this snippet and share your triumph on social media!
                  </p>
                  <textarea rows="3" style="width:100%; background:#333; color:#FFF;">{share_msg}</textarea>
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------------
# Main Streamlit app
# ---------------------
def main():
    st.set_page_config(page_title="Archer’s Paradox", layout="centered")
    st.title("Archer’s Paradox")

    # 1) Initialize session state
    if "current_file" not in st.session_state:
        st.session_state.current_file = "intro.json"
    if "story_data" not in st.session_state:
        st.session_state.story_data = load_json_file(st.session_state.current_file)
    if "current_node" not in st.session_state:
        st.session_state.current_node = "root"

    if "points" not in st.session_state:
        st.session_state.points = 0
    if "inventory" not in st.session_state:
        st.session_state.inventory = []
    if "visited_nodes" not in st.session_state:
        st.session_state.visited_nodes = set()

    # ------------------------------
    # Sidebar with Logo
    # ------------------------------
    with st.sidebar:
        st.image(
            "assets/mobilelogo.png",
            width=200
        )
        st.header("Player Stats")
        st.write(f"**Points:** {st.session_state.points}")

        if st.session_state.inventory:
            st.write("**Inventory:**")
            for item in st.session_state.inventory:
                st.write(f"- {item}")
        else:
            st.write("**Inventory:** (empty)")

        # Collapsible box for Save/Load
        with st.expander("Save / Load Progress", expanded=False):
            # Load
            upload_file = st.file_uploader("Load a previously saved JSON", type=["json"])
            if upload_file is not None:
                try:
                    data = json.load(upload_file)
                    st.session_state.points = data.get("points", 0)
                    st.session_state.inventory = data.get("inventory", [])
                    st.session_state.current_file = data.get("file", "intro.json")
                    st.session_state.current_node = data.get("node", "root")
                    st.session_state.story_data = load_json_file(st.session_state.current_file)
                    st.session_state.visited_nodes.clear()
                    st.success("Progress loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load progress: {e}")

            # Save
            if st.button("Save My Progress"):
                progress_data = {
                    "points": st.session_state.points,
                    "inventory": st.session_state.inventory,
                    "file": st.session_state.current_file,
                    "node": st.session_state.current_node,
                }
                download_str = json.dumps(progress_data, indent=2)
                st.download_button(
                    label="Download Progress JSON",
                    data=download_str,
                    file_name="archers_paradox_progress.json",
                    mime="application/json"
                )

        # ---- "Share This Moment" (PDF) ----
        #if st.button("Share This Moment"):
        #    node_data = get_node_data(st.session_state.story_data, st.session_state.current_node)
        #    pdf_buffer = generate_pdf(
        #        st.session_state.points,
        #        st.session_state.inventory,
        #        st.session_state.current_node,
        #        node_data
        #    )
        #    st.download_button(
        #        label="Download Archer’s Reflection (PDF)",
        #       data=pdf_buffer,
        #        file_name="Archer_Paradox_Reflection.pdf",
        #       mime="application/pdf"
        #    )

    # 2) Retrieve the current node data
    node_data = get_node_data(st.session_state.story_data, st.session_state.current_node)

    # 3) Display story text in a dark "card"
    story_text = node_data.get("text", "No text found for this node.")
    st.markdown(
        f"""
        <div style='background-color:#333333; 
                    border-radius:10px; 
                    padding:20px; 
                    margin-bottom:20px;
                    border: 1px solid #555;
                    color: #ffffff;'>
            {story_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4) Apply rewards/consequences if first time
    if st.session_state.current_node not in st.session_state.visited_nodes:
        apply_rewards_and_consequences(node_data)
        st.session_state.visited_nodes.add(st.session_state.current_node)

    # 5) Display choices as buttons (with item gating)
    choices = node_data.get("choices", {})
    if choices:
        st.subheader("Choices:")
        for choice_label, choice_value in choices.items():
            if choice_value.endswith(".json"):
                # Directly load a new JSON file
                if st.button(choice_label):
                    set_current_story(choice_value)
                    st.rerun()
            else:
                # Node within the same JSON
                if can_access_node(st.session_state.story_data, choice_value):
                    if st.button(choice_label):
                        st.session_state.current_node = choice_value
                        st.rerun()
                else:
                    st.button(f"{choice_label} (Locked)", disabled=True)

if __name__ == "__main__":
    main()
