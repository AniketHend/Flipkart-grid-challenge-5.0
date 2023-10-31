import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv("newdata.csv",sep="\t")

# Create interaction matrix and find similarity
interaction_matrix = data.pivot_table(index='User ID', columns='book id', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get product recommendations based on product name and category
def get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity, num_recommendations=50):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by product name and category
    filtered_products = filter_by_product_name_and_category(recommended_products, product_name, category)
    
    return filtered_products

# Function to filter recommended products by product name and category
def filter_by_product_name_and_category(products, product_name, category):
    filtered_products = data[data['book name'] == product_name]
    filtered_products = filtered_products[filtered_products['author'] == category]
    return filtered_products

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Fashion Product Recommender",
        page_icon="🛍️",
        
    )

    
    st.title("Fashion Product Recommender")
    st.markdown("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    product_name = st.selectbox("Select Product Name", data['book name'].unique())
    category = st.selectbox("Select Category", data['author'].unique())
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity)
        
        if len(recommendations) > 10:
            random_recommendations = random.sample(list(recommendations['book id']), 10)
        else:
            random_recommendations = list(recommendations['book id'])
        
        # Display recommended products
        st.subheader("Recommended Products:")
        recommended_products_info = data[data['book id'].isin(random_recommendations)][['book id', 'book name', 'author', 'genre', 'publication']]
        st.table(recommended_products_info)
        
        # Display user's history
        st.subheader("User History:")
        user_products_info = data[data['User ID'] == user_id][['book name', 'author', 'genre', 'publication']].drop_duplicates()
        st.table(user_products_info)

if __name__ == "__main__":
    main()
