import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
TILE_WIDTH = "500px"
MAX_GRID_WIDTH = "1200PX"
HEADER_SIZE = "36px"
SIDEBAR_FONT = "14px"
REGIONS = ["Capital City", "Green Valley", "Cactus Canyon", "Sunny Isles", "Frosty Fjords", "Limestone Cliffs"]

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

    # -- FARMER'S MARKET --
    "Vegetables": {"ing": {"Seeds": 2}, "t": 20, "b": "Farmer's Market"},
    "Flour Bag": {"ing": {"Seeds": 2, "Textiles": 2}, "t": 30, "b": "Farmer's Market"},
    "Fruit & Berries": {"ing": {"Seeds": 2, "Tree Saplings": 1}, "t": 90, "b": "Farmer's Market"},
    "Cream": {"ing": {"Animal Feed": 1}, "t": 75, "b": "Farmer's Market"},
    "Cheese": {"ing": {"Animal Feed": 2}, "t": 105, "b": "Farmer's Market"},
    "Beef": {"ing": {"Animal Feed": 3}, "t": 150, "b": "Farmer's Market"},

    # -- FURNITURE STORE --
    "Chairs": {"ing": {"Wood": 2, "Nails": 1, "Hammer": 1}, "t": 20, "b": "Furniture Store"},
    "Tables": {"ing": {"Planks": 1, "Nails": 2, "Hammer": 1}, "t": 30, "b": "Furniture Store"},
    "Home Textiles": {"ing": {"Textiles": 2, "Measuring Tape": 1}, "t": 75, "b": "Furniture Store"},
    "Cupboard": {"ing": {"Planks": 2, "Glass": 2, "Paint": 1}, "t": 45, "b": "Furniture Store"},
    "Couch": {"ing": {"Textiles": 3, "Drill": 1, "Glue": 1}, "t": 150, "b": "Furniture Store"},

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

    # -- REGIONAL ITEMS --
    "Reusable Bag": {"ing": {"Recycled Fabric": 2}, "t": 20, "b": "Eco Shop"},
    "Ecological Shoes": {"ing": {"Recycled Fabric": 2, "Glue": 1, "Measuring Tape": 1}, "t": 45, "b": "Eco Shop"},
    "Yoga Mat": {"ing": {"Recycled Fabric": 3, "Home Textiles": 1, "Paint": 1}, "t": 90, "b": "Eco Shop"},
    "Motor Oil": {"ing": {"Crude Oil": 2}, "t": 60, "b": "Car Parts Shop"},
    "Car Tire": {"ing": {"Crude Oil": 2, "Glue": 2, "Nails": 3}, "t": 90, "b": "Car Parts Shop"},
    "Engine": {"ing": {"Electrical Components": 1, "Drill": 1, "Nails": 3}, "t": 180, "b": "Car Parts Shop"},
}

SHOP_COLORS = {
    "Factory": "#E0E0E0", "Building Supplies": "#FFCCBC", "Hardware Store": "#D1C4E9",
    "Farmer's Market": "#C8E6C9", "Furniture Store": "#BBDEFB", "Donut Shop": "#F8BBD0",
    "Fast Food": "#FFF9C4"
}
SHOPS = sorted(list(set(details["b"] for details in RECIPES.values())))
ITEM_LIST = [""] + sorted(list(RECIPES.keys()))

st.set_page_config(layout="wide", page_title="SimCity BuildIt Planner by sgx")

# --- 3. CSS (Max Tile Size & Grid Logic) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
<style>
    .stApp {{ background-color: #F4F7F6 !important; }}
    * {{ color: black !important; font-family: 'Montserrat', sans-serif !important; }}
    
    /* Grid Container with Max Width */
    .flex-grid {{ 
        display: flex; 
        flex-wrap: wrap; 
        gap: 16px; 
        justify-content: flex-start; 
        margin-bottom: 30px; 
        max-width: {MAX_GRID_WIDTH}; 
    }}

    /* Global Input Styling */
    div[data-baseweb="select"], div[data-baseweb="input"], input, .stNumberInput div {{
        border: 1px solid #333333;
        border-radius: 1px;
        background-color: white !important;
        min-height: 24px !important;
    }}

    /* Remove plus/minus buttons */
    button[step] {{ display: none !important; }}
    input[type=number] {{ -moz-appearance: textfield !important; text-align: center !important; }}
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button {{ -webkit-appearance: none !important; margin: 0 !important; }}

    /* Tile Container sizing */
    div[data-testid="stVerticalBlockBorder"] {{
        border: 1px solid black;
        border-radius: 1px;
        background-color: white !important;
        box-shadow: 1px 1px 1px 1px,black;
        width: 40px; 
        flex: 1; 
        margin: 1px;
    }}

    .tile-header {{
        padding: 15px 5px; border-bottom: 4px solid black; text-align: center;
        min-height: 90px; display: flex; flex-direction: column; justify-content: center;
    }}
    .tile-header-main {{ font-size: {HEADER_SIZE}; font-weight: 800; }}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 📦 Warehouse")
    if 'inv' not in st.session_state: st.session_state.inv = {itm: 0 for itm in RECIPES}
    if 'prod' not in st.session_state: st.session_state.prod = {itm: 0 for itm in RECIPES}
    
    c1, c2, c3 = st.columns([3, 1.2, 1.2])
    c1.caption("Item")
    c2.caption("Have")
    c3.caption("Prod")

    for itm in sorted(RECIPES.keys()):
        col1, col2, col3 = st.columns([3, 1.2, 1.2])
        col1.markdown(f"<div style='margin-top:4px; font-size:16px;'>{itm}</div>", unsafe_allow_html=True)
        st.session_state.inv[itm] = col2.number_input("", 0, 999, key=f"inv_{itm}", label_visibility="collapsed")
        st.session_state.prod[itm] = col3.number_input("", 0, 999, key=f"prd_{itm}", label_visibility="collapsed")

# --- 5. TILE COMPONENT ---
def render_tile(line1, line2, key, color="#FFFFFF", icon="", can_add=False, is_res=False):
    slot_count = st.session_state.get(f"slots_{key}", 3)
    items = []
    is_done = st.session_state.get(f"done_{key}", False)
    opacity = "0.4" if is_done else "1.0"
    
    with st.container(border=True):
        st.markdown(f'''<div class="tile-header" style="background-color: {color}; opacity: {opacity};">
                        <div class="tile-header-main">{icon} {line1}</div>
                        <div style="font-size:18px; opacity:0.7;">{line2}</div>
                    </div>''', unsafe_allow_html=True)
        
        st.markdown(f'<div style="padding: 8px; opacity: {opacity};">', unsafe_allow_html=True)
        
        source_suffix = ""
        if is_res:
            reg = st.selectbox("Region", REGIONS, key=f"reg_{key}", label_visibility="collapsed", disabled=is_done)
            source_suffix = f" ({reg})"

        cb1, cb2 = st.columns(2)
        priority = cb1.checkbox("Prio", key=f"prio_{key}", disabled=is_done)
        done = cb2.checkbox("Done", key=f"done_{key}")
            
        for i in range(slot_count):
            r1, r2 = st.columns([3, 1])
            itm = r1.selectbox("Item", ITEM_LIST, key=f"{key}_i{i}", label_visibility="collapsed", disabled=is_done)
            qty = r2.number_input("Qty", 0, 999, key=f"{key}_q{i}", label_visibility="collapsed", disabled=is_done)
            if itm and qty > 0 and not is_done: 
                items.append({"item": itm, "qty": qty, "priority": priority, "source": f"{line1} {line2}{source_suffix}"})
                
        if can_add and not is_done:
            if st.button("＋ Item", key=f"btn_{key}"):
                st.session_state[f"slots_{key}"] = slot_count + 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    return items

# --- 6. MAIN APP ---
st.title("SimCity BuildIt Planner")
t_ord, t_res, t_exp, t_ana = st.tabs(["🚀 Orders", "🏠 Residential", "🚛 Export", "📊 Analysis"])

if 'hq_count' not in st.session_state: st.session_state.hq_count = 1

with t_ord:
    all_o = []
    st.markdown("### Delivery Tasks")
    st.write('<div class="flex-grid">', unsafe_allow_html=True)
    all_o += render_tile("War", "Deliveries", "war", "#FFCDD2", "⚔️")
    all_o += render_tile("Cargo", "Ship", "ship", "#C8E6C9", "🚢")
    all_o += render_tile("London", "Airport", "lon", "#BBDEFB", "✈️")
    all_o += render_tile("Tokyo", "Airport", "tok", "#BBDEFB", "✈️")
    all_o += render_tile("Paris", "Airport", "par", "#BBDEFB", "✈️")
    st.write('</div>', unsafe_allow_html=True)

    st.markdown("### Epic Project")
    st.write('<div class="flex-grid">', unsafe_allow_html=True)
    all_o += render_tile("Epic", "Special Project", "epic", "#FFE0B2", "💎", can_add=True)
    st.write('</div>', unsafe_allow_html=True)

with t_res:
    all_res = []
    st.write('<div class="flex-grid">', unsafe_allow_html=True)
    for i in range(8):
        all_res += render_tile("Residential", f"Unit {i+1}", f"res_{i}", "#E1BEE7", "🏠", can_add=True, is_res=True)
    st.write('</div>', unsafe_allow_html=True)

with t_exp:
    all_exp = []
    st.markdown("### Regional Exports")
    st.write('<div class="flex-grid">', unsafe_allow_html=True)
    all_exp += render_tile("Export", "Green Valley", "exp_gv", "#F0F4C3", "🍃")
    all_exp += render_tile("Export", "Cactus Canyon", "exp_cc", "#F0F4C3", "🌵")
    all_exp += render_tile("Export", "Sunny Isles", "exp_si", "#F0F4C3", "☀️")
    all_exp += render_tile("Export", "Frosty Fjords", "exp_ff", "#F0F4C3", "❄️")
    all_exp += render_tile("Export", "Limestone", "exp_lc", "#F0F4C3", "🗿")
    st.write('</div>', unsafe_allow_html=True)
    
    st.markdown("### Export HQ")
    if st.button("＋ Add HQ Tile"):
        st.session_state.hq_count += 1
        st.rerun()
    st.write('<div class="flex-grid">', unsafe_allow_html=True)
    for i in range(st.session_state.hq_count):
        all_exp += render_tile("Export", f"HQ {i+1}", f"hq_{i}", "#D1C4E9", "🏢")
    st.write('</div>', unsafe_allow_html=True)

with t_ana:
    st.markdown("### 🏗️ Shop Capacities")
    cap_cols = st.columns(len(SHOPS))
    shop_caps = {shop: cap_cols[i].number_input(shop, 1, 11, value=3, key=f"cap_{shop}") for i, shop in enumerate(SHOPS)}

    if st.button("🚀 RUN ANALYSIS", use_container_width=True):
        master = {}
        prio_items = set()

        def solve(itm, q, is_prio, source):
            if not itm or itm not in RECIPES: return
            if itm not in master: master[itm] = {"total": 0, "sources": []}
            master[itm]["total"] += q
            master[itm]["sources"].append(source)
            if is_prio: prio_items.add(itm)
            for ing, amt in RECIPES[itm]["ing"].items(): solve(ing, amt * q, is_prio, source)

        for o in (all_o + all_res + all_exp): 
            solve(o['item'], o['qty'], o.get('priority', False), o['source'])
        
        final = []
        for itm, data in master.items():
            needed = data["total"] - st.session_state.inv.get(itm, 0) - st.session_state.prod.get(itm, 0)
            if needed > 0:
                shop = RECIPES[itm]["b"]
                batches = -(-needed // shop_caps.get(shop, 3)) 
                final.append({
                    "Prio": "🔴" if itm in prio_items else "⚪", "Item": itm, "Needed": int(needed),
                    "Shop": shop, "Batches": f"{int(batches)}", "Source": ", ".join(set(data["sources"]))
                })
        
        if final: st.table(pd.DataFrame(final).sort_values(["Prio", "Shop"]))
        else: st.success("All requirements met!")

