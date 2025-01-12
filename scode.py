import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Recommendation Function
def recommend_random_heroes(data, filter_column, filter_value, n=1):
    filtered_data = data[data[filter_column] == filter_value]
    if filtered_data.empty:
        return pd.DataFrame()
    return filtered_data.sample(n=min(n, len(filtered_data)))

# Function to create a visual representation of difficulty
def difficulty_bar(difficulty):
    st.markdown(f"""
    <div style="width:100%; background-color:#e0e0e0; border-radius:5px;">
        <div style="width:{difficulty*10}%; background-color:#4CAF50; height:20px; border-radius:5px;"></div>
    </div>
    """, unsafe_allow_html=True)

# Function to create pie chart for win rate
def win_rate_pie_chart(win_rate):
    win_rate_label = ['Win Rate', 'Lose Rate']
    win_rate_values = [win_rate, 100 - win_rate]
    
    fig, ax = plt.subplots()
    ax.pie(win_rate_values, labels=win_rate_label, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF6347'])
    ax.axis('equal')
    
    st.pyplot(fig)

# Function to create pie chart for pick rate
def pick_rate_pie_chart(pick_rate):
    pick_rate_label = ['Pick Rate', 'No Pick']
    pick_rate_values = [pick_rate, 100 - pick_rate]
    
    fig, ax = plt.subplots()
    ax.pie(pick_rate_values, labels=pick_rate_label, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF6347'])
    ax.axis('equal')
    
    st.pyplot(fig)

# Function to create pie chart for ban rate
def ban_rate_pie_chart(ban_rate):
    ban_rate_label = ['Ban Rate', 'No Ban']
    ban_rate_values = [ban_rate, 100 - ban_rate]
    
    fig, ax = plt.subplots()
    ax.pie(ban_rate_values, labels=ban_rate_label, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF6347'])
    ax.axis('equal')
    
    st.pyplot(fig)

# Function to format the values correctly
def format_value(value):
    if isinstance(value, float):
        return f"{value:g}"  
    return value

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
        hero = recommendations.iloc[0] 
        icon = role_icons.get(hero['role'], "🎮")
        st.markdown(f"""
        ### {icon} {hero['hero_name']}
        """)
        st.markdown(f"""
                <h3 style="font-size: 20px; font-weight: bold;">Role: {hero['role']}</h3>
                <h3 style="font-size: 20px; font-weight: bold;">Counter Hero: {hero['counter']}</h3>
            """, unsafe_allow_html=True)
        st.markdown(f"""**Difficulty**: {hero['difficulty_overall']} """)
        difficulty_bar(hero['difficulty_overall'])
        
        # Create and display pie charts for win rate, pick rate, and ban rate
        win_rate_pie_chart(hero['win_rate'])
        pick_rate_pie_chart(hero['pick_rate'])
        ban_rate_pie_chart(hero['ban_rate'])

         # Format the hero stats into a table
        hero_stats = {
            "Informasi Lain": ["HP", "HP Regen", "Mana", "Mana Regen", "Movement Speed", 
                     "Magic Defense", "Physical Attack", "Physical Defense", 
                     "Attack Speed", "Release Year"],
            "Nilai": [format_value(hero['hp']), format_value(hero['hp_regen']), 
                      format_value(hero['mana']), format_value(hero['mana_regen']), 
                      format_value(hero['movement_spd']), format_value(hero['magic_defense']), 
                      format_value(hero['physical_atk']), format_value(hero['physical_defense']), 
                      format_value(hero['attack_speed']), format_value(hero['release_year'])]
        }

        # Create and display the table
        hero_stats_df = pd.DataFrame(hero_stats)
        st.table(hero_stats_df)


    else:
        st.warning(f"Tidak ada hero yang cocok untuk {filter_option.lower()}!")
