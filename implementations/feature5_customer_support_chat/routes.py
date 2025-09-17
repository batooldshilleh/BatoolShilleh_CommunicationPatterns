from flask import Blueprint, request
from flask_socketio import join_room, leave_room, emit
from app import db, socketio
from  app.models import ChatRoom, ChatMessage, User

bp = Blueprint('feature5_chat', __name__, url_prefix='/api/chat')

@bp.route('/create_room', methods=['POST'])
def create_room():
    data = request.json
    agent_id = data.get('agent_id')
    
    # تحقق من وجود العميل
    customer = User.query.get(data['customer_id'])
    if not customer:
        return {'error': 'Customer not found'}, 400
    
    # تحقق من وجود الوكيل إذا تم تمريره
    if agent_id:
        agent = User.query.get(agent_id)
        if not agent:
            return {'error': 'Agent not found'}, 400
    
    room = ChatRoom(customer_id=customer.id, agent_id=agent_id)
    db.session.add(room)
    db.session.commit()
    return {'room_id': room.id}, 201

@socketio.on('join_chat')
def handle_join_chat(data):
    room_id = data.get('room_id')
    user_type = data.get('user_type')  
    join_room(str(room_id))
    emit('status', {'msg': f'{user_type} joined room {room_id}'}, room=str(room_id))

@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room_id']
    sender_type = data['sender_type']
    content = data['content']

    msg = ChatMessage(room_id=room_id, sender_type=sender_type, content=content)
    db.session.add(msg)
    db.session.commit()

    emit('new_message', {
        'id': msg.id,
        'sender_type': sender_type,
        'content': content,
        'created_at': msg.created_at.isoformat()
    }, room=str(room_id))

@socketio.on('typing')
def handle_typing(data):
    room_id = data['room_id']
    user_type = data['user_type']
    emit('typing', {'user_type': user_type}, room=str(room_id), include_self=False)

@socketio.on('delivered')
def handle_delivered(data):
    msg_id = data['message_id']
    msg = ChatMessage.query.get(msg_id)
    if msg:
        msg.delivered = True
        db.session.commit()
        emit('delivered_ack', {'message_id': msg_id}, room=str(msg.room_id))
