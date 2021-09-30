from flask import Blueprint, render_template, flash,request, jsonify    #Blue print for our application it has bunch of roots inside ,, bunch of URL... splitof multiple files
from flask_login import  login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)

@views.route('/', methods=  ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user)

@views.route( '/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  #because data not coming as form so using json
    noteID = note['noteId']

    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

