from flask import Blueprint, request, jsonify, Response
from src.database import db
from src.models import Animal

api = Blueprint('api', __name__, template_folder='api')

@api.route('/', methods=['GET', 'POST'])
def get_create():
    if request.method == 'POST':
        try:
            name = request.json['name'].strip()
            if len(name) < 2:
                return Response(status=400)
            
            new_animal = Animal(
                name=name,
                description=request.json['description'].strip(),
                image_url=request.json['image_url'].strip(),
            )
            db.session.add(new_animal)
            db.session.commit()
            return jsonify({
                'id': new_animal.id,
                'name': new_animal.name,
                'description': new_animal.description,
                'image_url': new_animal.image_url,
                'created_at': new_animal.created_at
            }), 201

        except:
            return Response(status=400)
            
    else:
        search = request.args.get('search') if request.args.get('search') is not None else ''
        limit = request.args.get('limit')

        if limit:
            try:
                limit = int(limit)
                if limit > 0:
                    animals = Animal.query.filter(Animal.name.like(f'%{search}%') | Animal.description.like(f'%{search}%')).order_by(Animal.created_at).limit(limit).all()
                else:
                    return Response(status=400)
            except:
                return Response(status=400)
        else:
            animals = Animal.query.filter(Animal.name.like(f'%{search}%') | Animal.description.like(f'%{search}%')).order_by(Animal.created_at).all()

        return jsonify([
            {
                'id': animal.id,
                'name': animal.name,
                'description': animal.description,
                'image_url': animal.image_url,
                'created_at': animal.created_at
            }
            for animal in animals]
        )


@api.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def show_update_delete(id):
    selected_animal = Animal.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({
            'id': selected_animal.id,
            'name': selected_animal.name,
            'description': selected_animal.description,
            'image_url': selected_animal.image_url,
            'created_at': selected_animal.created_at
        })

    elif request.method == 'PUT':
        try:
            name = request.json['name'].strip()
            if len(name) < 2:
                return Response(status=400)

            selected_animal.name = name
            selected_animal.description = request.json['description'].strip()
            selected_animal.image_url = request.json['image_url'].strip()
            db.session.commit()
            
            return jsonify({
                'id': selected_animal.id,
                'name': selected_animal.name,
                'description': selected_animal.description,
                'image_url': selected_animal.image_url,
                'created_at': selected_animal.created_at
            })
        except:
            return Response(status=400)

    else:
        try:
            db.session.delete(selected_animal)
            db.session.commit()
            return Response(status=204)

        except:
            return Response(status=400)