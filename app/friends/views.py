from . import friends_bp

from flask import render_template

@friends_bp.route('/') 
def friends(): 
    return render_template("friends.html", title="friends")