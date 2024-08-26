from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient('mongodb+srv://rajpawar1808:5sWeHSaIqUJYUCD3@cluster0.q4bj0fh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['chef_master_db']
dishes = db['dishes']

# List of sample dishes
sample_dishes = [
    {"name": "Spaghetti Carbonara", "cuisine": "Italian", "difficulty": "Medium"},
    {"name": "Chicken Tikka Masala", "cuisine": "Indian", "difficulty": "Medium"},
    {"name": "Caesar Salad", "cuisine": "American", "difficulty": "Easy"},
    {"name": "Beef Stroganoff", "cuisine": "Russian", "difficulty": "Medium"},
    {"name": "Vegetable Stir Fry", "cuisine": "Chinese", "difficulty": "Easy"},
    {"name": "Margherita Pizza", "cuisine": "Italian", "difficulty": "Medium"},
    {"name": "Sushi Rolls", "cuisine": "Japanese", "difficulty": "Hard"},
    {"name": "Pad Thai", "cuisine": "Thai", "difficulty": "Medium"},
    {"name": "Beef Tacos", "cuisine": "Mexican", "difficulty": "Easy"},
    {"name": "Ratatouille", "cuisine": "French", "difficulty": "Medium"},
    {"name": "Greek Salad", "cuisine": "Greek", "difficulty": "Easy"},
    {"name": "Beef Wellington", "cuisine": "British", "difficulty": "Hard"},
    {"name": "Kung Pao Chicken", "cuisine": "Chinese", "difficulty": "Medium"},
    {"name": "Lasagna", "cuisine": "Italian", "difficulty": "Medium"},
    {"name": "Fish and Chips", "cuisine": "British", "difficulty": "Medium"}
]

# Generate sample data
data_to_insert = []
for i in range(30):  # Generate 30 entries
    dish = random.choice(sample_dishes)
    data_to_insert.append({
        "name": dish["name"],
        "date": datetime.now() - timedelta(days=i),
        "cuisine": dish["cuisine"],
        "difficulty": dish["difficulty"],
        "rating": random.randint(1, 5),
        "cooking_time": random.randint(15, 120)  # in minutes
    })

# Insert data into MongoDB
result = dishes.insert_many(data_to_insert)

print(f"Inserted {len(result.inserted_ids)} documents into the dishes collection.")

# Verify the insertion by printing a few entries
print("\nSample entries:")
for dish in dishes.find().limit(5):
    print(f"{dish['name']} - {dish['date'].strftime('%Y-%m-%d')} - {dish['cuisine']} - {dish['difficulty']}")