import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy


data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 4],
    'item_id': [101, 102, 103, 101, 104, 102, 103, 101],
    'rating': [5, 3, 4, 2, 4, 5, 3, 4]
}
ratings_df = pd.DataFrame(data)


reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(ratings_df[['user_id', 'item_id', 'rating']], reader)


trainset, testset = train_test_split(dataset, test_size=0.25)


model = SVD()
model.fit(trainset)


predictions = model.test(testset)
accuracy.rmse(predictions)


all_item_ids = ratings_df['item_id'].unique()

def recommend(user_id, model, ratings_df, n=10):
    
    rated_item_ids = ratings_df[ratings_df['user_id'] == user_id]['item_id'].unique()

    unrated_item_ids = [item_id for item_id in all_item_ids if item_id not in rated_item_ids]

    predictions = [model.predict(user_id, item_id) for item_id in unrated_item_ids]

    predictions.sort(key=lambda x: x.est, reverse=True)

  
    top_n_recommendations = predictions[:n]

    recommended_item_ids = [pred.iid for pred in top_n_recommendations]
    return recommended_item_ids


user_id = 1  
top_10_recommendations = recommend(user_id, model, ratings_df, n=10)
print("Top 10 item recommendations for user {}: {}".format(user_id, top_10_recommendations))
