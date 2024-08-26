from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from app.models import RecipeModel
import logging

from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

data = {
    'dish_name': ['Pasta Carbonara', 'Chicken Curry', 'Caesar Salad', 'Beef Stir Fry'],
    'recipe': [
        'To make Pasta Carbonara, start by cooking 400g of spaghetti in salted boiling water until al dente. Meanwhile, in a large pan, fry 150g of diced pancetta or guanciale until crispy. In a bowl, whisk together 4 large eggs, 50g of grated Pecorino Romano, and 50g of grated Parmesan cheese. Season with freshly ground black pepper. Drain the pasta, reserving a cup of pasta water. Quickly toss the hot pasta with the crispy pancetta, then remove from heat and pour in the egg and cheese mixture, stirring rapidly to create a creamy sauce. If needed, add a splash of reserved pasta water to reach desired consistency. Serve immediately with extra grated cheese and black pepper on top.',
        
        'For Chicken Curry, begin by marinating 500g of diced chicken breast in a mixture of 2 tbsp yogurt, 1 tsp turmeric, and 1 tsp garam masala for 30 minutes. In a large pot, heat 2 tbsp of oil and fry 1 diced onion until golden. Add 3 minced garlic cloves and 1 tbsp grated ginger, cooking for another minute. Stir in 2 tbsp of curry powder and cook until fragrant. Add the marinated chicken and cook until sealed. Pour in 400ml of coconut milk and 200ml of chicken stock. Simmer for 20 minutes until the chicken is cooked through and the sauce has thickened. Season with salt to taste and stir in a handful of chopped cilantro. Serve hot with steamed basmati rice and naan bread.',
        
        'To prepare a classic Caesar Salad, start by making the dressing. In a bowl, whisk together 1 egg yolk, 2 minced garlic cloves, 2 tsp Dijon mustard, 2 tsp Worcestershire sauce, the juice of 1 lemon, and 1/2 tsp anchovy paste. Slowly drizzle in 1/2 cup of olive oil while whisking to emulsify. Season with salt and black pepper. For the salad, wash and chop 2 heads of romaine lettuce. Toss the lettuce with the dressing, making sure each leaf is well coated. Add 1 cup of garlic croutons and 1/2 cup of freshly grated Parmesan cheese. Toss again lightly. For the chicken, season 2 chicken breasts with salt and pepper, then grill until cooked through. Slice and place on top of the salad. Finish with extra Parmesan shavings and freshly ground black pepper.',
        
        'For a delicious Beef Stir Fry, start by slicing 500g of beef sirloin into thin strips. Marinate the beef in a mixture of 2 tbsp soy sauce, 1 tbsp oyster sauce, and 1 tsp sesame oil for 15 minutes. Heat 2 tbsp of vegetable oil in a wok over high heat. Add 2 minced garlic cloves and 1 tbsp grated ginger, stir-frying for 30 seconds. Add the marinated beef and stir-fry for 2-3 minutes until browned. Remove the beef and set aside. In the same wok, stir-fry a mix of vegetables: 1 sliced bell pepper, 1 sliced onion, 1 cup of broccoli florets, and 1 cup of snap peas. Cook for 3-4 minutes until crisp-tender. Return the beef to the wok. Mix 1/4 cup of chicken stock with 1 tbsp cornstarch and add to the wok, stirring until the sauce thickens. Season with additional soy sauce if needed. Serve hot over steamed rice, garnished with sliced green onions and sesame seeds.'
    ]
}
df = pd.DataFrame(data)

recipe_model = RecipeModel()

try:
    recipe_model.train(df['dish_name'], df['recipe'])
    app.logger.info("Model trained successfully")
except Exception as e:
    app.logger.error(f"Error training model: {str(e)}")

#route
@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    try:
        data = request.json
        dish_name = data.get('dish')
        if not dish_name:
            return jsonify({'error': 'No dish name provided'}), 400
        
        recipe = recipe_model.generate_recipe(dish_name)
        if recipe is None:
            return jsonify({'error': 'Recipe not found'}), 404
        return jsonify({'recipe': recipe})
    except Exception as e:
        app.logger.error(f"Error generating recipe: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/', methods=['GET'])
def home():
    return "Recipe Generator is running!"


#MongoDB

#connection
client = MongoClient('mongodb+srv://rajpawar1808:5sWeHSaIqUJYUCD3@cluster0.q4bj0fh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['chef_master_db']
dishes = db['dishes']

@app.route('/api/dish_history', methods=['GET','POST'])
def get_dish_history():
    try:
        # Test database connection
        if db.command('ping'):
            print("Pinged your deployment. You successfully connected to MongoDB!")
        else:
            return jsonify({"error": "Failed to connect to MongoDB"}), 500

        dishes_cursor = dishes.find().sort("date", -1).limit(5)
        dishes_list = json.loads(json_util.dumps(dishes_cursor))
        
        if not dishes_list:
            print("No dishes found in the database")
            return jsonify({"dishes": []}), 200

        for dish in dishes_list:
            if 'date' in dish and '$date' in dish['date']:
                dish['date'] = dish['date']['$date'][:10]
            else:
                dish['date'] = 'Unknown'
        
        return jsonify({"dishes": dishes_list})
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)