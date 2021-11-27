from flask import Blueprint, render_template, request, redirect
from src.database import db
from src.models import Animal

base = Blueprint('base', __name__, template_folder='base')

@base.route('/', methods=['GET'])
def index():
    search = request.args.get('search') if request.args.get('search') is not None else ''
    animals = Animal.query.filter(Animal.name.like(f'%{search}%') | Animal.description.like(f'%{search}%')).order_by(Animal.created_at).all()
    return render_template('pages/index.html', animals=animals, search=search)


@base.route('/<int:id>/', methods=['GET'])
def show(id):
    animal = Animal.query.get(id)
    return render_template('pages/show.html', animal=animal)


@base.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            if len(name) < 2:
                return render_template('pages/create_update.html', error='Name requires at least 2 characters.')

            new_animal = Animal(
                name=name,
                description=request.form['description'].strip(),
                image_url=request.form['image_url'].strip(),
            )
            db.session.add(new_animal)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding that animal.'
    else:
        return render_template('pages/create_update.html')


@base.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    animal_to_delete = Animal.query.get_or_404(id)

    if request.method == 'POST':
        try:
            db.session.delete(animal_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that animal.'

    else:
        return render_template('pages/delete.html', animal=animal_to_delete)


@base.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    animal_to_update = Animal.query.get_or_404(id)

    if request.method == 'POST':
    
        try:
            name = request.form['name'].strip()
            if len(name) < 2:
                return render_template(
                    'pages/create_update.html',
                    animal=animal_to_update,
                    error='Name requires at least 2 characters.'
                )
            animal_to_update.name = name
            animal_to_update.description = request.form['description'].strip()
            animal_to_update.image_url = request.form['image_url'].strip()
        
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that animal.'

    else:
        return render_template('pages/create_update.html', animal=animal_to_update)


@base.route('/about/', methods=['GET'])
def about():
    return render_template('pages/about.html')


@base.route('/about-api/', methods=['GET'])
def about_api():
    return render_template('pages/about_api.html')