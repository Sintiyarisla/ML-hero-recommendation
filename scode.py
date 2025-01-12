import pandas as pd
import streamlit as st

# Recommendation Function
def recommend_random_heroes(data, filter_column, filter_value, n=1):
    filtered_data = data[data[filter_column] == filter_value]
    if filtered_data.empty:
        return pd.DataFrame()
    return filtered_data.sample(n=min(n, len(filtered_data)))

# Load Dataset
file_path = 'mlbb_heros.csv'  
data = pd.read_csv(file_path)
data = data.dropna(subset=['role', 'lane'])

# Streamlit Page Setup
st.set_page_config(
    page_title="Rekomendasi Hero Mobile Legends",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏆 Rekomendasi Hero Mobile Legends")
st.markdown("Pilih **Role** atau **Lane** untuk mendapatkan rekomendasi hero Mobile Legends.")

# Pilihan Filter (Role or Lane)
filter_option = st.radio("Pilih cara rekomendasi:", ("Berdasarkan Role 🦸🏻", "Berdasarkan Lane 🌌"))

# Pilihan Role or Lane 
recommendations = None
if filter_option == "Berdasarkan Role 🦸🏻":
    roles = sorted(data['role'].unique())
    selected_role = st.selectbox("Pilih Role:", roles)
    recommendations = recommend_random_heroes(data, 'role', selected_role, n=1)
else:
    lanes = sorted(data['lane'].unique())
    selected_lane = st.selectbox("Pilih Lane:", lanes)
    recommendations = recommend_random_heroes(data, 'lane', selected_lane, n=1)

# Icon
role_icons = {
    "Fighter": "⚔️",
    "Mage": "🪄",
    "Marksman": "🏹",
    "Tank": "🛡️",
    "Support": "🕊️",
    "Assassin": "🗡️"
}

# Tombol untuk mendapatkan rekomendasi
if st.button("🔍 Dapatkan Rekomendasi"):
    if recommendations is not None and not recommendations.empty:
        hero = recommendations.iloc[0]  # Ambil hero pertama
        icon = role_icons.get(hero['role'], "🎮")
        st.markdown(f"""
        ### {icon} {hero['hero_name']}
        **Role**: {hero['role']}   
        **Difficulty**: {hero['difficulty_overall']}  
        **Movement Speed**: {hero['movement_spd']}  
        **Magic Defense**: {hero['magic_defense']}  
        **Mana**: {hero['mana']}  
        **HP Regen**: {hero['hp_regen']}  
        **Physical Attack**: {hero['physical_atk']}  
        **Physical Defense**: {hero['physical_defense']}  
        **HP**: {hero['hp']}  
        **Attack Speed**: {hero['attack_speed']}  
        **Mana Regen**: {hero['mana_regen']}  
        **Win Rate**: {hero['win_rate']}%  
        **Pick Rate**: {hero['pick_rate']}%  
        **Ban Rate**: {hero['ban_rate']}%  
        **Release Year**: {hero['release_year']}  
        """)
    else:
        st.warning(f"Tidak ada hero yang cocok untuk {filter_option.lower()}!")
