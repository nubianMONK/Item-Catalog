from flask_restful import abort
import requests
from catalog.catalogapp import bp
from catalog.catalogapp.forms import EditItemForm, AddItemForm, AddCategoryForm
from flask import (render_template, request, redirect, url_for, flash,
                   current_app, jsonify)
from flask_login import login_required, current_user


# Helper functions:

# fetch all categories via the Catalog RESTFUL API service
def all_categories():
    # Make a get request to the API endpoint
    resp = requests.get(current_app.config['API_ADDRESS'] +
                        '/api/v1/categories')
    if resp.status_code != 200:
        flash('GET /categories/ {}'.format(resp.status_code))
    categories = resp.json()
    for k, v in categories.items():
        sub_list = v
    return sub_list


# Fetch all items via the Catalog Catalog RESTFUL API service
def all_items():
    # Make a get request to the API endpoint
    resp = requests.get(current_app.config['API_ADDRESS'] +
                        '/api/v1/items')
    if resp.status_code != 200:
        flash('GET /items/ {}'.format(resp.status_code))
    items = resp.json()
    for k, v in items.items():
        sub_list = v
    return sub_list


# Fetch an item via the Catalog API
def one_item(id):
    # Make a get request to the Catalog RESTFUL API endpoint
    sub_uri = '/api/v1/items/{}'.format(id)
    resp = requests.get(current_app.config['API_ADDRESS'] + sub_uri)
    if resp.status_code != 200:
        flash('GET /item/ {}'.format(resp.status_code))
    item = resp.json()
    for k, v in item.items():
        sub_list = v
    return sub_list


# Fetch Catalog Data via the Catalog RESTFUL API service
def fetch_json(uri):
    resp = requests.get(uri)
    if resp.status_code != 200:
        flash('GET /item/ {}'.format(resp.status_code))
    item = resp.json()
    return item


# Fetch Items by Category via the Catalog RESTFUL API service
def _items_by_catagory(id):
    sub_uri = '/api/v1/categories/{}/items'.format(id)
    uri = current_app.config['API_ADDRESS'] + sub_uri
    resp = requests.get(uri)
    if resp.status_code != 200:
        flash('GET /items by category/ {}'.format(resp.status_code))
    items_by_category = resp.json()
    for k, v in items_by_category.items():
        sub_list = v
    return sub_list


# Route Views:

# Home page view
@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
                        'catalogapp/index.html',
                        all_categories=all_categories(), all_items=all_items()
                            )


# Item view
@bp.route('/catalog/category/item/<int:id>', methods=['GET', 'POST'])
def item(id):
    item = one_item(id)
    return render_template('catalogapp/item_information.html',
                           item=item
                           )


# Items by Category view
@bp.route('/catalog/category/<int:id>/items', methods=['GET', 'POST'])
def items_by_category(id):
    items_by_category = _items_by_catagory(id)
    return render_template('catalogapp/items_by_category.html',
                           all_categories=all_categories(),
                           items_by_category=items_by_category
                           )


# Item Edit view
@bp.route('/catalog/category/item/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    # Instantiate a WTF Form
    form = EditItemForm(request.form)
    categories = all_categories()
    item = one_item(id)

    # Fetch All Categories and make a list of Categories
    category_list = \
        [(category['id'], category['category_name'])
            for category in categories]
    # Dynamically create and populate the WTF SelectField
    # Needed to populate a dropdown list of categories
    form.category_name.choices = category_list
    form.category_name.choices.insert(
        0, (item['item_category']['id'],
            item['item_category']['category_name'])
                                        )

    if request.method == 'POST':
        if form.validate_on_submit():
            sub_uri = '/api/v1/items/{}'.format(id)
            uri = current_app.config['API_ADDRESS'] + sub_uri
            # Using the HTTP method/verb PUT edit an item
            # via the the Catalog RESTFUL API service
            resp = requests.put(uri,
                                json={
                                        'item_name': form.item_name.data,
                                        'item_description':
                                        form.item_description.data,
                                        'category_id': form.category_name.data}
                                )

            if resp.status_code != 200:
                flash('Item Update Operation failed with code {}'
                      .format(resp.status_code))
                abort(404, message="Item not successfully updated")
            flash('Item Update successful')
            return redirect(url_for('catalogapp.index'))

    form.item_name.data = item['item_name']
    form.item_description.data = item['item_description']
    return render_template('catalogapp/edit_item.html', form=form, item=item)


# Item Addition view
@bp.route('/catalog/category/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItemForm(request.form)
    categories = all_categories()
    category_list = [(category['id'], category['category_name'])
                     for category in categories]
    form.category_name.choices = category_list

    if request.method == 'POST':
        if form.validate_on_submit():
            sub_uri = '/api/v1/items'
            uri = current_app.config['API_ADDRESS'] + sub_uri

            # Using the HTTP method/verb POST to Add an item
            # via the the Catalog RESTFUL API service
            resp = requests.post(uri, json={
                                        'item_name': form.item_name.data,
                                        'item_description':
                                        form.item_description.data,
                                        'user_id': current_user.id,
                                        'category_id': form.category_name.data
                                })

            if resp.status_code != 200:
                flash('Item Creation Operation failed with code {}'
                      .format(resp.status_code))
                abort(404, message="Item not successfully created")
            flash('Item Created successfully')
            return redirect(url_for('catalogapp.index'))
    return render_template('catalogapp/add_item.html', form=form)


# Item Delete view
@bp.route('/catalog/category/item/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    # Fetch Item to be deleted via the helper function
    # which uses a RESTful API service
    item = one_item(id)

    if request.method == 'POST':
        sub_uri = '/api/v1/items/{}'.format(id)
        uri = current_app.config['API_ADDRESS'] + sub_uri
        # Using the HTTP method/verb DELETE an item is deleted
        # via the the Catalog RESTFUL API service
        resp = requests.delete(uri)
        if resp.status_code != 200:
            flash('Item Delete Operation failed with code {}'
                  .format(resp.status_code))
            abort(404, message="Item not successfully deleted")
        flash('Item Delete Operation is successful')
        return redirect(url_for('catalogapp.index'))
    return render_template('catalogapp/delete_item_confirmation.html',
                           item=item)


# Add Category view
@bp.route('/catalog/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            sub_uri = '/api/v1/categories'
            uri = current_app.config['API_ADDRESS'] + sub_uri
            # Using the HTTP method/verb POST to Add a category
            # via the the Catalog RESTFUL API service
            resp = requests.post(uri, json={
                                            'category_name':
                                            form.category_name.data}
                                 )

            if resp.status_code != 200:
                flash('Category Creation Operation failed with code {}'
                      .format(resp.status_code))
                abort(404, message="Category not successfully created")
            flash('Category Created successfully')
            return redirect(url_for('catalogapp.index'))
    return render_template('catalogapp/add_category.html', form=form)


# Catalog JSON view
@bp.route('/catalog.json', methods=['GET'])
def json_endpoint():
    # Helper function leverages the Catalog RESTFUL API to fetch data
    data = fetch_json(current_app.config['API_ADDRESS'] + '/api/v1/catalog')
    return jsonify(data)
