import streamlit as st
import pandas as pd
import random

# Load data
data = pd.read_csv("newdata.csv",encoding="utf-8")

# Function to get popular books in the same genre
def get_recommendations(book_name, genre, num_recommendations=2):
    filtered_books = data[(data['genre'] == genre) & (data['book name'] != book_name)]
    if filtered_books.empty:
        return None
    
    popular_recommendations = filtered_books.nlargest(num_recommendations, 'Rating')[['book name', 'genre']]
    return popular_recommendations

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Book Recommender",
        page_icon="📚",
    )

    st.title("Book Recommender")
    st.markdown("Discover personalized book recommendations.")
    
    # User input
    book_name = st.selectbox("Select Book Name", data['book name'].unique())
    genre = st.selectbox("Select Genre", data['genre'].unique())
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(book_name, genre)
        
        if recommendations is not None and not recommendations.empty:
            st.subheader("Recommended Books:")
            st.table(recommendations)
        else:
            st.subheader("No Recommendations Found")

if __name__ == "__main__":
    main()
