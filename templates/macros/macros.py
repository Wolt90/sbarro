from flask import Blueprint, render_template_string

macros_bp = Blueprint('macros', __name__)

@macros_bp.app_template_global()
def user_table(user_data):
    return render_template_string('user_table.html', user_data=user_data)
