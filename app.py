import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
TILE_WIDTH = "500px"
MAX_GRID_WIDTH = "1200px"
HEADER_SIZE = "36px"
SIDEBAR_FONT = "14px"
REGIONS = [
    "Capital City",
    "Green Valley",
    "Cactus Canyon",
    "Sunny Isles",
    "Frosty Fjords",
    "Limestone Cliffs",
]
# --- 1. THE COMPLETE RECIPE DATABASE (2025 Edition) ---
# Format: "Item": {"ing": {Ingredients}, "t": Base Time in Minutes, "b": Building}
RECIPES = {
    # -- FACTORY (RAW MATERIALS) --
    "Metal": {"ing": {}, "t": 1, "b": "Factory"},
    "Wood": {"ing": {}, "t": 3, "b": "Factory"},
    "Plastic": {"ing": {}, "t": 9, "b": "Factory"},
    "Seeds": {"ing": {}, "t": 20, "b": "Factory"},
    "Minerals": {"ing": {}, "t": 30, "b": "Factory"},
    "Chemicals": {"ing": {}, "t": 120, "b": "Factory"},
    "Textiles": {"ing": {}, "t": 180, "b": "Factory"},
    "Sugar & Spices": {"ing": {}, "t": 240, "b": "Factory"},
    "Glass": {"ing": {}, "t": 300, "b": "Factory"},
    "Animal Feed": {"ing": {}, "t": 360, "b": "Factory"},
    "Electrical Components": {"ing": {}, "t": 420, "b": "Factory"},

    # -- BUILDING SUPPLIES --
    "Nails": {"ing": {"Metal": 2}, "t": 5, "b": "Building Supplies"},
    "Planks": {"ing": {"Wood": 2}, "t": 30, "b": "Building Supplies"},
    "Bricks": {"ing": {"Minerals": 2}, "t": 20, "b": "Building Supplies"},
    "Cement": {"ing": {"Minerals": 2, "Chemicals": 1}, "t": 50, "b": "Building Supplies"},
    "Glue": {"ing": {"Plastic": 1, "Chemicals": 2}, "t": 60, "b": "Building Supplies"},
    "Paint": {"ing": {"Metal": 2, "Minerals": 1, "Chemicals": 2}, "t": 60, "b": "Building Supplies"},

    # -- HARDWARE STORE --
    "Hammer": {"ing": {"Metal": 1, "Wood": 1}, "t": 14, "b": "Hardware Store"},
    "Measuring Tape": {"ing": {"Metal": 1, "Plastic": 1}, "t": 20, "b": "Hardware Store"},
    "Shovel": {"ing": {"Metal": 1, "Wood": 1, "Plastic": 1}, "t": 30, "b": "Hardware Store"},
    "Cooking Utensils": {"ing": {"Metal": 2, "Plastic": 2, "Wood": 2}, "t": 45, "b": "Hardware Store"},
    "Ladder": {"ing": {"Metal": 2, "Planks": 2}, "t": 60, "b": "Hardware Store"},
    "Drill": {"ing": {"Metal": 2, "Plastic": 2, "Electrical Components": 1}, "t": 120, "b": "Hardware Store"},
    "Drill": {"ing": {"Star Decoration": 1, "Wood": 2}, "t": 120, "b": "Hardware Store"},

    # -- FARMER'S MARKET --
    "Vegetables": {"ing": {"Seeds": 2}, "t": 20, "b": "Farmer's Market"},
    "Flour Bag": {"ing": {"Seeds": 2, "Textiles": 2}, "t": 30, "b": "Farmer's Market"},
    "Fruit & Berries": {"ing": {"Seeds": 2, "Tree Saplings": 1}, "t": 90, "b": "Farmer's Market"},
    "Cream": {"ing": {"Animal Feed": 1}, "t": 75, "b": "Farmer's Market"},
    "Cheese": {"ing": {"Animal Feed": 2}, "t": 105, "b": "Farmer's Market"},
    "Beef": {"ing": {"Animal Feed": 3}, "t": 150, "b": "Farmer's Market"},
    "Sock Decoration": {"ing": {"Star Decoration": 1, "Gift": 1, "Nails": 1}, "t": 150, "b": "Farmer's Market"},


    # -- FURNITURE STORE --
    "Chairs": {"ing": {"Wood": 2, "Nails": 1, "Hammer": 1}, "t": 20, "b": "Furniture Store"},
    "Tables": {"ing": {"Planks": 1, "Nails": 2, "Hammer": 1}, "t": 30, "b": "Furniture Store"},
    "Home Textiles": {"ing": {"Textiles": 2, "Measuring Tape": 1}, "t": 75, "b": "Furniture Store"},
    "Cupboard": {"ing": {"Planks": 2, "Glass": 2, "Paint": 1}, "t": 45, "b": "Furniture Store"},
    "Couch": {"ing": {"Textiles": 3, "Drill": 1, "Glue": 1}, "t": 150, "b": "Furniture Store"},

# -- GARDENING SUPPLIES --
    "Grass": {"ing": {"Seeds": 1, "Shovel": 1}, "t": 30, "b": "Gardening Supplies"},
    "Tree Saplings": {"ing": {"Seeds": 2, "Shovel": 1}, "t": 90, "b": "Gardening Supplies"},
    "Garden Furniture": {"ing": {"Planks": 2, "Plastic": 2, "Textiles": 2}, "t": 135, "b": "Gardening Supplies"},
    "Fire Pit": {"ing": {"Bricks": 2, "Shovel": 1, "Cement": 2}, "t": 240, "b": "Gardening Supplies"},
    "Lawn Mower": {"ing": {"Metal": 3, "Electrical Components": 1, "Paint": 1}, "t": 120, "b": "Gardening Supplies"},
    "Garden Gnome": {"ing": {"Cement": 2, "Glue": 1}, "t": 90, "b": "Gardening Supplies"},
    "Festive Wreath": {"ing": {"Star Decoration": 2, "Sock Decoration": 1, "Hammer": 1}, "t": 90, "b": "Gardening Supplies"},

	# -- FASHION STORE --
    "Cap": {"ing": {"Textiles": 2, "Measuring Tape": 1}, "t": 60, "b": "Fashion Store"},
    "Shoes": {"ing": {"Textiles": 2, "Glue": 1, "Measuring Tape": 1}, "t": 75, "b": "Fashion Store"},
    "Watch": {"ing": {"Plastic": 2, "Glass": 1, "Chemicals": 1}, "t": 90, "b": "Fashion Store"},
    "Business Suits": {"ing": {"Textiles": 3, "Glue": 1, "Measuring Tape": 1}, "t": 210, "b": "Fashion Store"},
    "Backpack": {"ing": {"Textiles": 2, "Plastic": 2, "Measuring Tape": 1}, "t": 150, "b": "Fashion Store"},
    "Gift Sled": {"ing": {"Star Decoration": 3, "Chair": 1, "Festive Wreath": 1}, "t": 150, "b": "Fashion Store"},

    # -- DONUT SHOP --
    "Donuts": {"ing": {"Flour Bag": 1, "Sugar & Spices": 1}, "t": 45, "b": "Donut Shop"},
    "Green Smoothie": {"ing": {"Vegetables": 1, "Fruit & Berries": 1}, "t": 30, "b": "Donut Shop"},
    "Bread Roll": {"ing": {"Flour Bag": 2, "Cream": 1}, "t": 60, "b": "Donut Shop"},
    "Cherry Cheesecake": {"ing": {"Flour Bag": 1, "Fruit & Berries": 1, "Cheese": 1}, "t": 90, "b": "Donut Shop"},
    "Coffee": {"ing": {"Seeds": 2, "Sugar & Spices": 1}, "t": 45, "b": "Donut Shop"},

    # -- FAST FOOD RESTAURANT --
    "Ice Cream Sandwich": {"ing": {"Bread Roll": 1, "Cream": 1}, "t": 14, "b": "Fast Food"},
    "Pizza": {"ing": {"Flour Bag": 1, "Cheese": 1, "Beef": 1}, "t": 24, "b": "Fast Food"},
    "Burgers": {"ing": {"Beef": 1, "Bread Roll": 1, "BBQ Grill": 1}, "t": 35, "b": "Fast Food"},
    "Cheese Fries": {"ing": {"Vegetables": 1, "Cheese": 1}, "t": 20, "b": "Fast Food"},
    "Popcorn": {"ing": {"Corn": 2, "Microwave Oven": 1}, "t": 30, "b": "Fast Food"},

# -- HOME APPLIANCES --
    "BBQ Grill": {"ing": {"Metal": 3, "Cooking Utensils": 1}, "t": 165, "b": "Home Appliances"},
    "Refrigerator": {"ing": {"Plastic": 2, "Chemicals": 2, "Electrical Components": 2}, "t": 210, "b": "Home Appliances"},
    "Lighting System": {"ing": {"Chemicals": 1, "Glass": 1, "Electrical Components": 1}, "t": 105, "b": "Home Appliances"},
    "TV": {"ing": {"Plastic": 2, "Glass": 2, "Electrical Components": 2}, "t": 150, "b": "Home Appliances"},
    "Microwave Oven": {"ing": {"Metal": 4, "Glass": 1, "Electrical Components": 1}, "t": 120, "b": "Home Appliances"},


# --- REGIONAL RAW MATERIALS (2025 UPDATED) ---
    "Recycled Fabric": {"ing": {}, "t": 6, "b": "Eco-Factory"},
    "Crude Oil": {"ing": {}, "t": 6, "b": "Oil Plant"},
    "Fish": {"ing": {}, "t": 6, "b": "Fishery"},
    "Coconut": {"ing": {}, "t": 6, "b": "Coconut Farm"},
    "Silk": {"ing": {}, "t": 6, "b": "Mulberry Grove"},

    # --- ECO SHOP (Green Valley) ---
    "Reusable Bag": {"ing": {"Recycled Fabric": 2}, "t": 16, "b": "Eco Shop"},
    "Ecological Shoes": {"ing": {"Recycled Fabric": 2, "Glue": 1, "Measuring Tape": 1}, "t": 90, "b": "Eco Shop"},
    "Yoga Mat": {"ing": {"Recycled Fabric": 3, "Home Textile": 2, "Paint": 1}, "t": 180, "b": "Eco Shop"},

    # --- CAR PARTS SHOP (Cactus Canyon) ---
    "Motor Oil": {"ing": {"Crude Oil": 2}, "t": 16, "b": "Car Parts Shop"},
    "Car Tire": {"ing": {"Crude Oil": 2, "Glue": 1, "Nails": 3}, "t": 96, "b": "Car Parts Shop"},
    "Engine": {"ing": {"Electrical Components": 1, "Drill": 1, "Nails": 3}, "t": 180, "b": "Car Parts Shop"},

    # --- FISHING MARKETPLACE (Frosty Fjords) ---
    "Canned Fish": {"ing": {"Fish": 1, "Metal": 1}, "t": 16, "b": "Fishing Marketplace"},
    "Fish Soup": {"ing": {"Fish": 2, "Vegetables": 1, "Cooking Utensils": 2}, "t": 90, "b": "Fishing Marketplace"},
    "Salmon Sandwich": {"ing": {"Fish": 2, "Bread Roll": 1}, "t": 180, "b": "Fishing Marketplace"},

    # --- TROPICAL PRODUCTS STORE (Sunny Isles) ---
    "Coconut Oil": {"ing": {"Coconut": 2}, "t": 16, "b": "Tropical Products Store"},
    "Face Cream": {"ing": {"Coconut Oil": 2, "Chemicals": 2}, "t": 90, "b": "Tropical Products Store"},
    "Tropical Drink": {"ing": {"Coconut": 2, "Fruit and Berries": 2, "Sugar and Spices": 1}, "t": 180, "b": "Tropical Products Store"},

    # --- SILK STORE (Limestone Cliffs) ---
    "String": {"ing": {"Silk": 2}, "t": 16, "b": "Silk Store"},
    "Fan": {"ing": {"Silk": 2, "Wood": 1, "Glue": 2}, "t": 90, "b": "Silk Store"},
    "Robe": {"ing": {"Silk": 3, "Paint": 2, "Home Textile": 1}, "t": 180, "b": "Silk Store"},
    
    # --- LONDON EXPORTS ---
    "London Bus": {"ing": {}, "t": 0, "b": "Airport (London)"},
    "Phone Box": {"ing": {}, "t": 0, "b": "Airport (London)"},
    "Tea": {"ing": {}, "t": 0, "b": "Airport (London)"},

    # --- PARIS EXPORTS ---
    "Baguette": {"ing": {}, "t": 0, "b": "Airport (Paris)"},
    "Beret": {"ing": {}, "t": 0, "b": "Airport (Paris)"},
    "La Tour Eiffel": {"ing": {}, "t": 0, "b": "Airport (Paris)"},

    # --- TOKYO EXPORTS ---
    "Maneki-neko": {"ing": {}, "t": 0, "b": "Airport (Tokyo)"},
    "Bonsai Tree": {"ing": {}, "t": 0, "b": "Airport (Tokyo)"},
    "Lantern": {"ing": {}, "t": 0, "b": "Airport (Tokyo)"},

    # --- RAILROAD ITEMS ---
    "Conducting Wand": {"ing": {}, "t": 0, "b": "Railroad Shop"},
    "Railroad Spike": {"ing": {}, "t": 0, "b": "Railroad Shop"},
    "Train Signal": {"ing": {}, "t": 0, "b": "Railroad Shop"},
    "Railroad Bolt": {"ing": {}, "t": 0, "b": "Railroad Shop"},
    "Hatches": {"ing": {}, "t": 0, "b": "Railroad Shop"}

}
# --- 3. SHOP COLORS ---
SHOP_COLORS = {
    "Factory": "#E0E0E0",
    "Building Supplies": "#FFCCBC",
    "Hardware Store": "#D1C4E9",
    "Farmer's Market": "#C8E6C9",
    "Furniture Store": "#BBDEFB",
    "Donut Shop": "#F8BBD0",
    "Fast Food": "#FFF9C4",
    "Fashion Store": "#F48FB1",
    "Gardening Supplies": "#A5D6A7",
    "Home Appliances": "#90A4AE",
    "Health & Beauty": "#80CBC4",
    "Sports Shop": "#E6EE9C",
    "Bureau of Restoration": "#D7CCC8",
    "Eco Shop": "#DCEDC8",
    "Car Parts Shop": "#FFCC80",
    "Fishing Marketplace": "#B3E5FC",
    "Tropical Products Store": "#FFF59D",
    "Silk Store": "#E1BEE7",
    "Airport (London)": "#EF9A9A",
    "Airport (Paris)": "#CE93D8",
    "Airport (Tokyo)": "#90CAF9",
    "Railroad Shop": "#BDBDBD"
}
SHOPS = sorted(list(set(details["b"] for details in RECIPES.values())))
ITEM_LIST = [""] + sorted(list(RECIPES.keys()))

st.set_page_config(layout="wide", page_title="SimCity BuildIt Planner by sgx")
# --- 3. STATE INITIALIZATION & FUNCTIONS ---
if "reset_ver" not in st.session_state: 
    st.session_state.reset_ver = 0

# Fix 1: Ensure this function is defined BEFORE Section 5 (the sidebar)
def reset_warehouse_only():
    """Wipes ONLY the inventory/production numbers."""
    st.session_state.inv = {itm: 0 for itm in RECIPES}
    st.session_state.prod = {itm: 0 for itm in RECIPES}
    # Fix 2: Removed the stray dot that was causing the SyntaxError
    st.session_state.reset_ver += 1
    st.rerun()

def force_reset():
    """Wipes everything: Warehouse AND Planning Tiles."""
    for key in list(st.session_state.keys()):
        if key != "reset_ver":
            del st.session_state[key]
    st.session_state.reset_ver += 1
    st.rerun()# --- 4. CSS ---
st.markdown("""
    <style>
    .tile-card { background: white; border: 1px solid #ddd; border-radius: 10px; padding: 8px; margin-bottom: 10px; }
    .tile-header { padding: 10px; border-radius: 8px 8px 0 0; text-align: center; font-weight: bold; margin: -8px -8px 10px -8px; }
    .analysis-html-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .analysis-html-table th, .analysis-html-table td { border: 1px solid #eee; padding: 6px; }
    div.stButton > button:first-child[key^="res_"] { background-color: #ff4b4b; color: white; border: none; }
    div.stButton > button:hover[key^="res_"] { background-color: #ff3333; color: white; }
    </style>
    """, unsafe_allow_html=True)



# --- 5. SIDEBAR (WAREHOUSE) ---
with st.sidebar:
    st.header("📦 Warehouse")
    
    # This button now ONLY clears the counts, not your planning tiles
    if st.button("🧹 Reset Warehouse", use_container_width=True, key="res_warehouse_only"):
        reset_warehouse_only()
     
    st.divider()
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.markdown("**ITEM**"); h2.markdown("**HAVE**"); h3.markdown("**PROD**")
    
    for itm in sorted(RECIPES.keys()):
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.markdown(f"<div style='font-size:12px; padding-top:5px;'>{itm}</div>", unsafe_allow_html=True)
        
        # We use .get() and reset_ver to ensure the boxes update immediately when cleared
        st.session_state.inv[itm] = c2.number_input(
            "H", 0, 999, 
            value=st.session_state.inv.get(itm, 0), 
            key=f"wh_{itm}_{st.session_state.reset_ver}", 
            label_visibility="collapsed"
        )
        st.session_state.prod[itm] = c3.number_input(
            "P", 0, 999, 
            value=st.session_state.prod.get(itm, 0), 
            key=f"pr_{itm}_{st.session_state.reset_ver}", 
            label_visibility="collapsed"
        )


# --- 6. RENDER FUNCTION ---
def render_tile(line1, line2, key, color="#FFFFFF", icon="", can_add=False, is_res=False):
    unique_id = f"tile_{key}_{line2.lower().replace(' ', '_')}"
    slot_key = f"slots_{unique_id}"
    if slot_key not in st.session_state: st.session_state[slot_key] = 3
    items_found = []
    st.markdown(f'<div class="tile-card"><div class="tile-header" style="background:{color}">{icon} {line1} - {line2}</div>', unsafe_allow_html=True)
    if is_res: st.selectbox("Region", REGIONS, key=f"reg_{unique_id}", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    prio, done = c1.checkbox("Priority", key=f"prio_{unique_id}"), c2.checkbox("Done", key=f"done_{unique_id}")
    for i in range(st.session_state[slot_key]):
        ci, cq = st.columns([3, 1])
        itm = ci.selectbox("Item", ITEM_LIST, key=f"i_{unique_id}_{i}", label_visibility="collapsed", disabled=done)
        qty = cq.number_input("Qty", 0, 99, key=f"q_{unique_id}_{i}", label_visibility="collapsed", disabled=done)
        if itm and qty > 0 and not done:
            items_found.append({"item": itm, "qty": qty, "priority": prio})
    if can_add and not done:
        if st.button("＋ Add Slot", key=f"btn_{unique_id}", use_container_width=True):
            st.session_state[slot_key] += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    return items_found

# --- 7. TABS ---
t_ord, t_res, t_exp, t_ana = st.tabs(["🚀 Orders", "🏠 Residential", "🚛 Exports", "📊 Analysis"])
all_reqs = []

with t_ord:
    if st.button("🗑️ Reset All App Data", key="res_ord", use_container_width=True): reset_all_data()
    o_cols = st.columns(2)
    specs = [("War", "Deliveries", "war", "#FFCDD2", "⚔️"), ("Cargo", "Ship", "ship", "#C8E6C9", "🚢"), ("London", "Airport", "lon", "#BBDEFB", "✈️"), ("Tokyo", "Airport", "tok", "#BBDEFB", "✈️"), ("Paris", "Airport", "par", "#BBDEFB", "✈️"), ("Epic", "Project", "epic", "#FFE0B2", "💎", True)]
    for idx, s in enumerate(specs):
        with o_cols[idx % 2]: all_reqs += render_tile(*s)

with t_res:
    if st.button("🗑️ Reset All App Data", key="res_res", use_container_width=True): reset_all_data()
    r_cols = st.columns(2)
    for i in range(6):
        with r_cols[i % 2]: all_reqs += render_tile("Residential", f"Unit {i+1}", f"res_{i}", "#E1BEE7", "🏠", True, True)

with t_exp:
    if st.button("🗑️ Reset All App Data", key="res_exp", use_container_width=True): reset_all_data()
    e_cols = st.columns(2)
    ex_specs = [("Export", "Green Valley", "gv", "#F0F4C3", "🍃"), ("Export", "Cactus Canyon", "cc", "#F0F4C3", "🌵"), ("Export", "Sunny Isles", "si", "#F0F4C3", "☀️"), ("Export", "Frosty Fjords", "ff", "#F0F4C3", "❄️"), ("Export", "Limestone", "lc", "#F0F4C3", "🗿")]
    for idx, s in enumerate(ex_specs):
        with e_cols[idx % 2]: all_reqs += render_tile(*s)
    for i in range(st.session_state.hq_count):
        with e_cols[i % 2]: all_reqs += render_tile("Export", f"HQ {i+1}", f"hq_{i}", "#D1C4E9", "🏢", True)
    if st.button("＋ Add HQ Tile"): st.session_state.hq_count += 1; st.rerun()

with t_ana:
    if st.button("🗑️ Reset All App Data", key="res_ana", use_container_width=True): reset_all_data()
    if st.button("🚀 RUN ANALYSIS", use_container_width=True, key="run_main"):
        master = {}
        prio_set = set()
        def solve(itm, q, p):
            if itm not in RECIPES: return
            if p: prio_set.add(itm)
            master[itm] = master.get(itm, 0) + q
            for ing, iq in RECIPES[itm].get("ing", {}).items(): solve(ing, iq * q, p)
        for task in all_reqs: solve(task['item'], task['qty'], task['priority'])
        
        final = []
        for itm, goal in master.items():
            h, p = st.session_state.inv.get(itm, 0), st.session_state.prod.get(itm, 0)
            diff = goal - h - p
            if diff > 0:
                final.append({"Priority": "🔴 High" if itm in prio_set else "⚪ Normal", "Item": itm, "Goal": int(goal), "Have": int(h), "Prod": int(p), "Make": int(diff), "Shop": RECIPES[itm]["b"], "Time": f"{int(RECIPES[itm]['t'] * diff)}m"})
        if final:
            df = pd.DataFrame(final).sort_values(["Priority", "Shop"])
            for index, row in df.iterrows():
                c = SHOP_COLORS.get(row['Shop'], "#E0E0E0")
                df.at[index, 'Shop'] = f'<span style="background-color:{c}; padding: 2px 8px; border-radius: 4px; color: black; font-weight: bold;">{row["Shop"]}</span>'
            st.write(df.to_html(escape=False, index=False, classes="analysis-html-table"), unsafe_allow_html=True)
        else:
            st.success("✅ Warehouse covers all needs!")