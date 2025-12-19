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

SHOP_COLORS = {
    # -- BASE GAME SHOPS --
    "Factory": "#E0E0E0",               # Light Grey
    "Building Supplies": "#FFCCBC",     # Deep Orange
    "Hardware Store": "#D1C4E9",        # Deep Purple
    "Farmer's Market": "#C8E6C9",       # Green
    "Furniture Store": "#BBDEFB",       # Blue
    "Donut Shop": "#F8BBD0",            # Pink
    "Fast Food": "#FFF9C4",             # Yellow
    "Fashion Store": "#F48FB1",         # Hot Pink
    "Gardening Supplies": "#A5D6A7",    # Pale Green
    "Home Appliances": "#90A4AE",       # Blue Grey
    "Health & Beauty": "#80CBC4",       # Teal

      # -- SPECIALTY SHOPS --
    "Sports Shop": "#E6EE9C",           # Lime Green
    "Bureau of Restoration": "#D7CCC8", # Brownish Grey (Old Town)

    # -- REGIONAL --
    "Eco Shop": "#DCEDC8",
    "Car Parts Shop": "#FFCC80",
    "Fishing Marketplace": "#B3E5FC",
    "Tropical Products Store": "#FFF59D",
    "Silk Store": "#E1BEE7",
SHOP_COLORS.update({
    "Airport (London)": "#EF9A9A", # Soft Red
    "Airport (Paris)": "#CE93D8",  # Soft Purple
    "Airport (Tokyo)": "#90CAF9",  # Soft Blue
    "Railroad Shop": "#BDBDBD"     # Grey
})
}

SHOPS = sorted(list(set(details["b"] for details in RECIPES.values())))
ITEM_LIST = [""] + sorted(list(RECIPES.keys()))

st.set_page_config(layout="wide", page_title="SimCity BuildIt Planner by sgx")

# --- 3. CSS & STYLING ---
st.markdown(
    f"""
<style>
    /* 1. Global App & Background */
    .stApp {{ 
        background-color: #F7FAFC !important; 
    }}
    
    /* Global Font Size Reduction for Mobile */
    html, body, [class*="css"] {{ 
        font-size: 13px !important; 
    }}

    /* 2. Grid & Row Alignment Fixes */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Forces side-by-side */
        align-items: stretch !important; /* Fixes vertical misalignment */
        gap: 8px !important;
        margin-bottom: 10px !important;
    }}
    
    [data-testid="column"] {{
        flex: 1 1 auto !important;
        width: fit-content !important;
        min-width: 0; /* Prevents columns from overflowing */
    }}

    /* 3. The Tile Card */
    .tile-card {{
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        width: 100%;
        height: 100%; /* Makes all tiles in a row equal height */
        margin-bottom: 15px;
        padding: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
    }}
    
    .tile-header {{
        padding: 10px;
        border-radius: 8px 8px 0 0;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        margin: -8px -8px 10px -8px; /* Flushes header to edges */
    }}

    /* 4. Mobile Widget Optimization */
    /* Shrink Selectboxes */
    .stSelectbox div[data-baseweb="select"] {{
        font-size: 12px !important;
        min-height: 32px !important;
    }}
    
    /* Shrink Number Inputs & Hide Arrows */
    .stNumberInput input {{
        height: 32px !important;
        font-size: 12px !important;
        -moz-appearance: textfield !important; 
        text-align: center !important;
        padding: 0 !important;
    }}
    
    /* Hide the [+] and [-] buttons on number inputs to save space */
    button[step] {{ 
        display: none !important; 
    }}

    /* Tighten Checkboxes (Priority/Done) */
    [data-testid="stCheckbox"] {{
        margin-bottom: 0px !important;
        padding: 2px !important;
        min-height: 0px !important;
    }}
    
    [data-testid="stCheckbox"] label p {{
        font-size: 12px !important;
        margin-bottom: 0px !important;
    }}

    /* Adjust Tab Font Size */
    button[data-baseweb="tab"] p {{
        font-size: 14px !important;
    }}

    /* Button Styling */
    .stButton button {{
        font-size: 12px !important;
        padding: 2px 10px !important;
        min-height: 30px !important;
    }}

</style>
""",
    unsafe_allow_html=True,
)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("📦 Warehouse")
    if "inv" not in st.session_state:
        st.session_state.inv = {itm: 0 for itm in RECIPES}
    if "prod" not in st.session_state:
        st.session_state.prod = {itm: 0 for itm in RECIPES}

    for itm in sorted(RECIPES.keys()):
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(itm)
        st.session_state.inv[itm] = c2.number_input(
            "H", 0, 999, key=f"inv_{itm}", label_visibility="collapsed"
        )
        st.session_state.prod[itm] = c3.number_input(
            "P", 0, 999, key=f"prd_{itm}", label_visibility="collapsed"
        )

# --- 5. RENDER FUNCTION (Fixed & Optimized) ---
def render_tile(line1, line2, key, color="#FFFFFF", icon="", can_add=False, is_res=False):
    # 1. Create a truly unique ID to prevent Duplicate Key Errors
    unique_id = f"{key}_{line1.lower().replace(' ', '')}"
    
    # 2. Manage Slot Count in Session State
    slot_key = f"slots_{unique_id}"
    if slot_key not in st.session_state: 
        st.session_state[slot_key] = 3
    
    slot_count = st.session_state[slot_key]
    items = []

    with st.container():
        # Open Tile Div with Custom Styling
        st.markdown(f'<div class="tile-card"><div class="tile-header" style="background:{color}">{icon} {line1} - {line2}</div>', unsafe_allow_html=True)
        
        # Region selection for Residential only
        if is_res:
            st.selectbox("Region", REGIONS, key=f"reg_{unique_id}", label_visibility="collapsed")
            
        # --- PRIORITY AND DONE ON ONE LINE ---
        c1, c2 = st.columns(2)
        with c1:
            prio = st.checkbox("Prio", key=f"prio_{unique_id}")
        with c2:
            done = st.checkbox("Done", key=f"done_{unique_id}")

        # --- ITEM AND QTY ROWS (SAME LINE) ---
        for i in range(slot_count):
            col_item, col_qty = st.columns([3, 1])
            with col_item:
                itm = st.selectbox(
                    "Item", ITEM_LIST, 
                    key=f"item_{unique_id}_{i}", 
                    label_visibility="collapsed", 
                    disabled=done
                )
            with col_qty:
                qty = st.number_input(
                    "Qty", 0, 99, 
                    key=f"qty_{unique_id}_{i}", 
                    label_visibility="collapsed", 
                    disabled=done
                )

            # Collect data if item is selected and tile isn't 'done'
            if itm and qty > 0 and not done:
                items.append({"item": itm, "qty": qty, "priority": prio, "source": line2})
        
        # --- ADD ITEM BUTTON ---
        if can_add and not done:
            # use_container_width makes it easier to tap on mobile
            if st.button("＋ Add Slot", key=f"btn_{unique_id}", use_container_width=True):
                st.session_state[slot_key] += 1
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    return items

# --- 6. MAIN APP LOGIC ---
st.title("SimCity BuildIt Planner")
# Added t_exp to the tabs
t_ord, t_res, t_exp, t_ana = st.tabs(["🚀 Orders", "🏠 Residential", "🚛 Exports", "📊 Analysis"])



all_o = []
all_res = []
all_exp = []
all_requirements = []



# 1. ORDERS TAB
with t_ord:
    st.markdown("### Delivery Tasks")
    o_cols = st.columns(3, gap='large')
    order_specs = [
        ("War", "Deliveries", "war", "#FFCDD2", "⚔️"),
        ("Cargo", "Ship", "ship", "#C8E6C9", "🚢"),
        ("London", "Airport", "lon", "#BBDEFB", "✈️"),
        ("Tokyo", "Airport", "tok", "#BBDEFB", "✈️"),
        ("Paris", "Airport", "par", "#BBDEFB", "✈️"),
        ("Epic", "Project", "epic", "#FFE0B2", "💎", True) # can_add=True
    ]
    for idx, spec in enumerate(order_specs):
        with o_cols[idx % 3]:
            # Unpack the spec tuple into the function
            all_requirements += render_tile(*spec)

# 2. RESIDENTIAL TAB
with t_res:
    st.markdown("### Residential Units")
    r_cols = st.columns(3, gap='large')
    for i in range(6):
        with r_cols[i % 3]:
            all_requirements += render_tile(
                "Residential", f"Unit {i+1}", f"res_{i}", "#E1BEE7", "🏠", 
                can_add=True, is_res=True
            )

# 3. EXPORT TAB
with t_exp:
    st.markdown("### Regional Exports")
    if 'hq_count' not in st.session_state: st.session_state.hq_count = 1
    
    e_cols = st.columns(3, gap='large')
    export_specs = [
        ("Export", "Green Valley", "exp_gv", "#F0F4C3", "🍃"),
        ("Export", "Cactus Canyon", "exp_cc", "#F0F4C3", "🌵"),
        ("Export", "Sunny Isles", "exp_si", "#F0F4C3", "☀️"),
        ("Export", "Frosty Fjords", "exp_ff", "#F0F4C3", "❄️"),
        ("Export", "Limestone", "exp_lc", "#F0F4C3", "🗿")
    ]
    for idx, spec in enumerate(export_specs):
        with e_cols[idx % 3]:
            all_requirements += render_tile(*spec)
            
    if st.button("＋ Add HQ Tile"):
        st.session_state.hq_count += 1
        st.rerun()

    for i in range(st.session_state.hq_count):
        with e_cols[(len(export_specs) + i) % 3]:
            all_requirements += render_tile("Export", f"HQ {i+1}", f"hq_{i}", "#D1C4E9", "🏢")
# --- 4. ANALYSIS TAB ---
with t_ana:
    st.markdown("### Resource Calculation")
    
    if st.button("🚀 RUN ANALYSIS", use_container_width=True):
        master = {}
        prio_items = set()

        # 1. DEFINE THE SOLVER
        def solve(itm, q, is_prio, source):
            if not itm or itm not in RECIPES: 
                return
            
            # Track priority items for highlighting later
            if is_prio: 
                prio_items.add(itm)
            
            # Add to master totals
            master[itm] = master.get(itm, 0) + q
            
            # Recursively solve for ingredients
            # 
            for ing, ing_qty in RECIPES[itm].get("ing", {}).items():
                solve(ing, ing_qty * q, is_prio, source)

        # 2. GATHER AND SOLVE
        # Combine all lists: all_o (Orders), all_res (Residential), and all_exp (Exports)
        # Note: Ensure these lists are initialized as [] at the top of your script!
        combined_tasks = all_requirements # Or (all_o + all_res + all_exp) depending on your setup
        
        for task in combined_tasks:
            solve(
                task['item'], 
                task['qty'], 
                task.get('priority', False), 
                task.get('source', 'General')
            )


        # 3. CALCULATE THE "FINAL" LIST AFTER SOLVING
        final = []
        for itm, total in master.items():
            # Calculate what we actually need to make
            have = st.session_state.inv.get(itm, 0)
            prod = st.session_state.prod.get(itm, 0)
            diff = total - have - prod
            
            if diff > 0:
                final.append({
                    "Priority": "🔴 High" if itm in prio_items else "⚪ Normal",
                    "Item": itm, 
                    "Make": int(diff), 
                    "Shop": RECIPES[itm]["b"], 
                    "Time": RECIPES[itm]['t'] * diff
                })

        # 4. DISPLAY THE DATA
        if final:
            df = pd.DataFrame(final).sort_values(["Priority", "Shop"], ascending=[True, True])
            
            # --- FACTORY TABLE ---
            st.subheader("🏭 Factory Queue")
            factory_df = df[df['Shop'] == 'Factory'][['Priority', 'Item', 'Make']]
            st.table(factory_df)
            
            # --- STORE TABLE ---
            st.subheader("🏪 Store Queue")
            df_shops = df[df['Shop'] != 'Factory'].copy()
            time_df = df_shops.copy() # Keep a numeric copy for the math below
            
            # Apply HTML badges for the UI
            for index, row in df_shops.iterrows():
                color = SHOP_COLORS.get(row['Shop'], "#E0E0E0")
                df_shops.at[index, 'Shop'] = f'<span style="background-color:{color}; padding: 2px 8px; border-radius: 4px; color: black;">{row["Shop"]}</span>'
                df_shops.at[index, 'Time'] = f"{int(row['Time'])}m"
            
            st.write(df_shops.to_html(escape=False, index=False), unsafe_allow_html=True)

            # --- TOTAL TIME LOAD ---
            st.markdown("---")
            st.subheader("⏱️ Total Shop Load")
            load = time_df.groupby("Shop")["Time"].sum().reset_index()
            load["Time"] = load["Time"].apply(lambda x: f"{int(x//60)}h {int(x%60)}m" if x >= 60 else f"{int(x)}m")
            st.table(load)
        else:
            st.success("✅ Your warehouse is fully stocked for these tasks!")