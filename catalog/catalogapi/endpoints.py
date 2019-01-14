from catalog import api
from datetime import datetime
import json
from flask_restful import reqparse, abort, Resource, fields, marshal, \
    marshal_with
from catalog.catalogapi.models import db, User, Item, Category, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)


# Fields
# Used to serialize returned data
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'picture': fields.String,
    'role': fields.String(default='User'),
    'self_uri': fields.Url('user', absolute=False),
    'items_uri': fields.Url('items_by_user', absolute=False)
}

item_fields = {
    'id': fields.Integer,
    'item_name': fields.String,
    'item_description': fields.String,
    'created_on': fields.DateTime(dt_format='rfc822'),
    'updated_on': fields.DateTime(dt_format='rfc822'),
    'self_uri': fields.Url('item', absolute=False),
    # Given an entity's backref property and corresponing fields
    # passed into a Nested field populates it
    'item_creator': fields.Nested(user_fields),

}

item_catalog_fields = {
    'id': fields.Integer,
    'item_name': fields.String,
    'item_description': fields.String,
    'category_id': fields.Integer,
    'user_id': fields.Integer
}

category_fields = {
    'id': fields.Integer,
    'category_name': fields.String,
    'self_uri': fields.Url('category', absolute=False),
    'items_uri': fields.Url('items_by_category', absolute=False)
}

# Item Fields updated with category information
item_fields.update({'item_category': fields.Nested(category_fields)})

catalog_fields = {
    'id': fields.Integer,
    'category_name': fields.String,
    'category_item': fields.Nested(item_catalog_fields)
}


# Resources:
# Grants access to multiple HTTP methods by defiining methods
# enabling CRUD resources


# User resource Api
class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='Username cannot be empty',
                                   location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='Email cannot be empty',
                                   location='json')
        self.reqparse.add_argument('picture', type=str, default='None',
                                   location='json')
        self.reqparse.add_argument('role', type=str, default='User',
                                   location='json')

        super().__init__()

    # HTTP methods/verbs
    def get(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        return {'user': marshal(user, user_fields)}

    def delete(self, id):
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        return {'result': True}

    @marshal_with(user_fields)
    def put(self, id):

        args = self.reqparse.parse_args()
        updated_username = str(args['username'])
        updated_email = str(args['email'])
        updated_picture = str(args['picture'])
        updated_role = str(args['role'])
        user = {'username': updated_username,
                'email': updated_email,
                'picture': updated_picture,
                'role': updated_role}
        keys = []
        for k, v in user.items():
            if v is None:
                keys.append(k)

        for key in keys:
            del user[key]

        db.session.query(User).filter_by(id=id).update(user)
        db.session.commit()
        updated_user = db.session.query(User).filter_by(id=id).first()
        return {'id': updated_user.id,
                'username': updated_user.username,
                'email': updated_user.email,
                'picture': updated_user.picture,
                'role': updated_user.role}


# User Collection Api
class UserListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='Username cannot be empty',
                                   location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='Email cannot be empty',
                                   location='json')
        self.reqparse.add_argument('picture', type=str, location='json')
        self.reqparse.add_argument('role', type=str, location='json')

        super().__init__()

# HTTP methods/verbs
    def get(self):
        users = db.session.query(User).all()
        return {'users': [marshal(user, user_fields) for user in users]}

    def post(self):
        args = self.reqparse.parse_args()
        user = User(username=args['username'], email=args['email'],
                    picture=args['picture'], role=args['role'])

        db.session.add(user)
        db.session.commit()
        return {'user': marshal(user, user_fields)}


# Items By User Api
class ItemsByUserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='Username cannot be empty',
                                   location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='Email cannot be empty',
                                   location='json')
        self.reqparse.add_argument('picture', type=str, location='json')
        self.reqparse.add_argument('role', type=str, location='json')

        super().__init__()

    # HTTP methods/verbs
    def get(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        items = user.items.all()
        return {'items': marshal(items, item_fields)}


# Item Collection Api
class ItemAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help='Item name cannot be empty',
                                   location='json')
        self.reqparse.add_argument('item_description', type=str, required=True,
                                   help='Item description cannot be empty',
                                   location='json')
        self.reqparse.add_argument('created_on', type=lambda x:
                                   datetime.strptime(x, "%Y-%m-%d").date(),
                                   location='json')
        self.reqparse.add_argument('updated_on', type=lambda x:
                                   datetime.strptime(x, "%Y-%m-%d").date(),
                                   default=datetime.utcnow(),
                                   location='json')
        self.reqparse.add_argument('category_id', type=int, required=False,
                                   help='Category id',
                                   location='json')

        super().__init__()

    # HTTP methods/verbs
    def get(self, id):
        item = db.session.query(Item).filter_by(id=id).first()
        return {'item': marshal(item, item_fields)}

    def delete(self, id):
        db.session.query(Item).filter_by(id=id).delete()
        db.session.commit()
        return {'result': True}

    @marshal_with(item_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        updated_item_name = str(args['item_name'])
        updated_item_description = str(args['item_description'])
        updated_date = str(args['updated_on'])
        updated_category_id = int(args['category_id'])
        item = {'item_name': updated_item_name,
                'item_description': updated_item_description,
                'updated_on': updated_date,
                'category_id': updated_category_id
                }
        keys = []
        for k, v in item.items():
            if v is None:
                keys.append(k)

        for key in keys:
            del item[key]

        db.session.query(Item).filter_by(id=id).update(item)
        db.session.commit()
        updated_item = db.session.query(Item).filter_by(id=id).first()
        return {'id': updated_item.id,
                'item_name': updated_item.item_name,
                'item_description': updated_item.item_description,
                'updated_on': updated_item.updated_on,
                'item_creator': updated_item.item_creator,
                'item_category': updated_item.item_category
                }


# Item Api
class ItemListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help='Item name cannot be empty',
                                   location='json')
        self.reqparse.add_argument('item_description', type=str, required=True,
                                   help='Item description cannot be empty',
                                   location='json')
        self.reqparse.add_argument('created_on', type=lambda x:
                                   datetime.strptime(x, "%Y-%m-%d").date(),
                                   location='json')
        self.reqparse.add_argument('updated_on', type=lambda x:
                                   datetime.strptime(x, "%Y-%m-%d").date(),
                                   location='json')
        self.reqparse.add_argument('user_id', type=int, required=True,
                                   help='User Id cannot be empty',
                                   location='json')
        self.reqparse.add_argument('category_id', type=int, required=True,
                                   help='Category Id cannot be empty',
                                   location='json')

        super().__init__()

    # HTTP methods/verbs
    def get(self):
        items = db.session.query(Item).all()
        return {'items': [marshal(item, item_fields) for item in items]}

    @marshal_with(item_fields)
    def post(self):
        args = self.reqparse.parse_args()
        item = Item(item_name=args['item_name'],
                    item_description=args['item_description'],
                    created_on=args['created_on'],
                    user_id=args['user_id'],
                    category_id=args['category_id']
                    )
        db.session.add(item)
        db.session.commit()
        data = {'id': item.id,
                'item_name': item.item_name,
                'item_description': item.item_description,
                'created_on': item.created_on,
                'updated_on': item.updated_on,
                'item_creator': item.item_creator,
                'item_category': item.item_category
                }
        return data


# Category Api
class CategoryAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('category_name', type=str, required=True,
                                   help='Category name cannot be empty',
                                   location='json')
        super().__init__()

    def get(self, id):
        category = db.session.query(Category).filter_by(id=id).first()
        return {'category': marshal(category, category_fields)}

    def delete(self, id):
        db.session.query(Category).filter_by(id=id).delete()
        db.session.commit()
        return {'result': True}

    def put(self, id):
        args = self.reqparse.parse_args()
        updated_category_name = str(args['category_name'])

        category = {'category_name': updated_category_name}

        db.session.query(Category).filter_by(id=id).update(category)
        db.session.commit()
        updated_category = db.session.query(Category).filter_by(id=id).first()
        return {'id': updated_category.id,
                'category_name': updated_category.category_name
                }


# Category Collection Api
class CategoryListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('category_name', type=str, required=True,
                                   help='Category name cannot be empty',
                                   location='json')
        super().__init__()

    # HTTP methods/verbs
    def get(self):
        categories = db.session.query(Category).all()
        return {'categories': [marshal(category, category_fields)
                               for category in categories]}

    def post(self):
        args = self.reqparse.parse_args()
        category = Category(category_name=args['category_name'])
        db.session.add(category)
        db.session.commit()
        return {'id': category.id,
                'category_name': category.category_name
                }


# Items by Category Api
class ItemsByCategoryAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('category_name', type=str, required=True,
                                   help='Category name cannot be empty',
                                   location='json')
        super().__init__()

    # HTTP methods/verbs
    def get(self, id):
        category = db.session.query(Category).filter_by(id=id).first()
        items = category.items.all()
        return {'items': marshal(items, item_fields)}


# Catalog JSON Api
class CatalogAPI(Resource):
    def get(self):
        categories = db.session.query(Category).all()
        return {'category': [marshal(category, catalog_fields)
                             for category in categories]}
