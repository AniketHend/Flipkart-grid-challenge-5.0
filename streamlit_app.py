import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

# Load data
data = pd.read_csv("newdata.csv")

# Create interaction matrix and find similarity
interaction_matrix = data.pivot_table(index='User ID', columns='book id', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get book recommendations based on book name and author
def get_recommendations(user_id, book_name, author, interaction_matrix, product_similarity, num_recommendations=2):
    if user_id not in interaction_matrix.index:
        return None
    
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_books = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended books by book name and author
    filtered_books = filter_by_book_name_and_author(recommended_books, book_name, author)
    
    return filtered_books

# Function to filter recommended books by book name and author
def filter_by_book_name_and_author(books, book_name, author):
    filtered_books = data[data['book name'] == book_name]
    filtered_books = filtered_books[filtered_books['author'] == author]
    return filtered_books['book id']

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Book Recommender",
        page_icon="📚",
    )

    st.title("Book Recommender")
    st.markdown("Discover personalized book recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    book_name = st.selectbox("Select Book Name", data['book name'].unique())
    author = st.selectbox("Select Author", data['author'].unique())
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, book_name, author, interaction_matrix, product_similarity)
        
        if recommendations is not None and len(recommendations) > 0:
            random_recommendations = random.sample(list(recommendations), min(2, len(recommendations)))
        
            # Display recommended books
            st.subheader("Recommended Books:")
            recommended_books_info = data[data['book id'].isin(random_recommendations)][['book id', 'book name', 'author', 'genre', 'Price', 'Rating', 'publication', 'number of pages']]
            
            if not recommended_books_info.empty:
                st.table(recommended_books_info)
            else:
                st.subheader("No Recommendations Found")
        else:
            st.subheader("No Recommendations Found")

if __name__ == "__main__":
    main()
