import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="CourtVision | Tennis Analytics",
    page_icon="🎾",
    layout="wide"
)

st.title("🎾 CourtVision Tennis Analytics Dashboard")
st.markdown("Explore professional tennis player career statistics and surface-specific performance breakdowns.")

# Load curated Gold layer data
@st.cache_data
def load_data():
    career_path = "data/curated/player_career_stats.csv"
    surface_path = "data/curated/player_surface_stats.csv"
    
    career_df = pd.read_csv(career_path) if os.path.exists(career_path) else pd.DataFrame()
    surface_df = pd.read_csv(surface_path) if os.path.exists(surface_path) else pd.DataFrame()
    
    return career_df, surface_df

career_df, surface_df = load_data()

if career_df.empty:
    st.warning("Curated career data not found. Please run your Gold layer transformation script first.")
else:
    # Sidebar player selection
    st.sidebar.header("Filter Options")
    player_list = sorted(career_df['player_name'].dropna().unique())
    selected_player = st.sidebar.selectbox("Select a Tennis Player", player_list)

    if selected_player:
        # Filter data for selected player
        player_career = career_df[career_df['player_name'] == selected_player]
        player_surface = surface_df[surface_df['player_name'] == selected_player] if not surface_df.empty else pd.DataFrame()

        st.header(f"Player Profile: {selected_player}")

        # High-level metrics row
        if not player_career.empty:
            row = player_career.iloc[0]
            col1, col2, col3 = st.columns(3)
            
            total_matches = row.get('total_matches', 0)
            total_wins = row.get('total_wins', 0)
            win_rate = (total_wins / total_matches * 100) if total_matches > 0 else 0

            col1.metric(label="Total Matches", value=int(total_matches))
            col2.metric(label="Total Wins", value=int(total_wins))
            col3.metric(label="Overall Win Rate", value=f"{win_rate:.1f}%")

        # Surface Performance Section
        st.subheader("Surface Breakdown")
        if not player_surface.empty:
            st.dataframe(player_surface, use_container_width=True)
            
            # Visualize wins by surface if columns exist
            if 'surface_name' in player_surface.columns and 'wins' in player_surface.columns:
                st.bar_chart(player_surface.set_index('surface_name')['wins'])
        else:
            st.info("No surface statistics available for this player.")