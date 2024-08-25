from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Task
from . import db
from sqlalchemy import or_
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    # Filtering options
    status = request.args.get('status')
    priority = request.args.get('priority')
    due_date = request.args.get('due_date')

    # Search options
    search = request.args.get('search')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    query = Task.query.filter_by(user_id=user_id)

    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if due_date:
        query = query.filter(Task.due_date == datetime.strptime(due_date, '%Y-%m-%d'))

    # Apply search
    if search:
        query = query.filter(or_(Task.title.ilike(f'%{search}%'), Task.description.ilike(f'%{search}%')))

    tasks = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "tasks": [{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            "created_at": task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for task in tasks.items],
        "total": tasks.total,
        "pages": tasks.pages,
        "current_page": tasks.page
    }), 200


@main.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'Todo'),
        priority=data.get('priority', 'Medium'),
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else None,
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201

@main.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else task.due_date

    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200

@main.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200