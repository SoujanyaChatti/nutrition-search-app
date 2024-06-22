from flask import Flask, render_template, request, redirect, url_for
import nutrition_search  # Import the Python script containing the search logic

app = Flask(__name__)

# List to store selected items' nutrient information
nutrient_items = []

# Route for the main index page displaying the search bar, search results, and nutrient table
@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []

    if request.method == 'POST':
        input_description = request.form.get('input_description')
        if input_description:
            matches = nutrition_search.prioritize_matches(input_description, nutrition_search.df)

    return render_template('index.html', matches=matches, nutrient_items=nutrient_items)

# Route to handle the addition of an item into the nutrition table
@app.route('/add_item', methods=['POST'])
def add_item():
    description = request.form['description']
    ndb_no = request.form['ndb_no']
    
    # Retrieve the nutrient information for the selected item
    nutrient_info = nutrition_search.df[nutrition_search.df['NDB_No'] == int(ndb_no)].iloc[0].to_dict()
    
    # Create a simplified dictionary for rendering in the table
    nutrient_item = {
        'description': description,
        'Water_(g)': nutrient_info.get('Water_(g)', 'N/A'),
        'Energ_Kcal': nutrient_info.get('Energ_Kcal', 'N/A'),
        'Protein_(g)': nutrient_info.get('Protein_(g)', 'N/A'),
        'Lipid_Tot_(g)': nutrient_info.get('Lipid_Tot_(g)', 'N/A'),
        'Carbohydrt_(g)': nutrient_info.get('Carbohydrt_(g)', 'N/A'),
        'Fiber_TD_(g)': nutrient_info.get('Fiber_TD_(g)', 'N/A'),
        'Vit_C_(mg)': nutrient_info.get('Vit_C_(mg)', 'N/A'),
        'Vit_A_IU': nutrient_info.get('Vit_A_IU', 'N/A'),
        'Vit_D_IU': nutrient_info.get('Vit_D_IU', 'N/A'),
        'Vit_E_(mg)': nutrient_info.get('Vit_E_(mg)', 'N/A'),
       
        'Vit_B6_(mg)': nutrient_info.get('Vit_B6_(mg)', 'N/A'),
      
        'Calcium_(mg)': nutrient_info.get('Calcium_(mg)', 'N/A'),
        'Iron_(mg)': nutrient_info.get('Iron_(mg)', 'N/A'),
        'Magnesium_(mg)': nutrient_info.get('Magnesium_(mg)', 'N/A'),
        'Phosphorus_(mg)': nutrient_info.get('Phosphorus_(mg)', 'N/A'),
        'Potassium_(mg)': nutrient_info.get('Potassium_(mg)', 'N/A'),
        'Sodium_(mg)': nutrient_info.get('Sodium_(mg)', 'N/A'),
        'Zinc_(mg)': nutrient_info.get('Zinc_(mg)', 'N/A'),
        'Quantity': 100# Default quantity
    }
    
    nutrient_items.append(nutrient_item)
    
    return redirect(url_for('index'))

# Route to handle removing an item from the nutrition table
@app.route('/remove_item', methods=['POST'])
def remove_item():
    index = int(request.form['index'])
    
    # Remove the item from the nutrient_items list based on the index
    if 0 <= index < len(nutrient_items):
        nutrient_items.pop(index)
    
    return redirect(url_for('index'))

# Route to handle updating the quantity of an item in the nutrition table
@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    index = int(request.form['index'])
    quantity = float(request.form['quantity'])
    
    if 0 <= index < len(nutrient_items):
        nutrient_items[index]['Quantity'] = quantity
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,port =8000)
    