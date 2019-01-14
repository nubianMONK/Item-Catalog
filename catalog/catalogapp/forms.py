from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length


class EditItemForm(FlaskForm):
    item_name = StringField('Title')
    item_description = TextAreaField('Description')
    category_name = SelectField('Category', coerce=int)
    submit = SubmitField('Submit')


class AddItemForm(FlaskForm):
    item_name = StringField(
        'Title', [
                    InputRequired('You did not provide an Item Title.'),
                    Length(
                        max=80, message='Max length of an Item Title  is 80.'
                           )
        ]
    )
    item_description = TextAreaField(
        'Description', [InputRequired('You did not provide a Description')])
    category_name = SelectField('Category', coerce=int)
    submit = SubmitField('Submit')


class AddCategoryForm(FlaskForm):
    category_name = StringField('Title', [InputRequired(
        'You did not provide a Category Title')]
                                )
    submit = SubmitField('Submit')
