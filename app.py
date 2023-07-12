from flask import Flask, jsonify, make_response, request
from config import db
from model.visitors import Visitor
from model.meeting import Meeting
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
app.app_context().push()
app.config.from_object('config')

class VisitorsScheme(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Visitor
        sql_session = db.session
        include_relationships = True
        load_instance = True
    ic = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    image = fields.String(required=True)

class MeetingScheme(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Meeting
        sql_session = db.session
    email = fields.String(required=True)
    time = fields.String(required=True)
    venue = fields.String(required=True)
    host = fields.String(required=True)

db.init_app(app)
# 
@app.route('/api/v1/visitor',methods=['POST'])
def new_visitor():
    data = request.get_json()
    visitor = Visitor(ic=data.get('ic'), email=data.get('email'), name=data.get('name'), image =data.get('image') )
    db.session.add(visitor)
    db.session.commit()
    visitor_schema = VisitorsScheme()
    result = visitor_schema.dump(visitor)
    return make_response(jsonify({"visitor": result}))

@app.route('/api/v1/visitor',methods=['GET'])
def visitor():
    get_visitor = Visitor.query.all()
    visitor_schema = VisitorsScheme(many=True)
    visitor = visitor_schema.dump(get_visitor)
    return make_response(jsonify({"visitors": visitor}))

@app.route('/api/v1/visitor/<ic>', methods=['GET'])
def visitor_by_ic(ic):
   get_visitor = Visitor.query.get(ic)
   visitor_schema = VisitorsScheme()
   visitor = visitor_schema.dump(get_visitor)
   return make_response(jsonify({"Visitor": visitor}))

@app.route('/api/v1/visitor/<ic>',methods=['PUT'])
def update_visitor_by_ic(ic):
    data = request.get_json()
    get_visitor = Visitor.query.get(ic)
    if data.get('name'):
        get_visitor.name = data['name']
    if data.get('email'):
        get_visitor.email = data['email']
    if data.get('image'):
        get_visitor.image = data['image']
    db.session.add(get_visitor)
    db.session.commit()
    visitor_schema = VisitorsScheme(only=['ic','name','email','image'])
    visitor = visitor_schema.dump(get_visitor)
    return make_response(jsonify({"visitor": visitor}))

@app.route('/api/v1/visitor/<ic>',methods=['DELETE'])
def delete_visitor(ic):
    get_visitor = Visitor.query.get(ic)
    db.session.delete(get_visitor)
    db.session.commit()
    return make_response("", 204)

@app.route('/api/v1/meeting',methods=['POST'])
def new_meeting():
    data = request.get_json()
    meeting = Meeting(email=data.get('email'), time=data.get('time'), venue=data.get('venue'), host =data.get('host') )
    db.session.add(meeting)
    db.session.commit()
    meeting_schema = MeetingScheme()
    meeting = meeting_schema.dump(meeting)
    return make_response(jsonify({"meeting": meeting}))

@app.route('/api/v1/meeting',methods=['GET'])
def meeting():
    get_meeting = Meeting.query.all()
    meeting_schema = MeetingScheme(many=True)
    meeting = meeting_schema.dump(get_meeting)
    return make_response(jsonify({"meeting": meeting}))

@app.route('/api/v1/meeting/<email>', methods=['GET'])
def meeting_by_email(email):
   get_meeting = Meeting.query.get(email)
   meeting_schema = MeetingScheme()
   meeting = meeting_schema.dump(get_meeting)
   return make_response(jsonify({"meeting": meeting}))

@app.route('/api/v1/meeting/<email>',methods=['PUT'])
def update_meeting_by_email(email):
    data = request.get_json()
    get_meeting = Meeting.query.get(email)
    if data.get('time'):
        get_meeting.time = data['time']
    if data.get('venue'):
        get_meeting.venue = data['venue']
    if data.get('host'):
        get_meeting.host = data['host']
    db.session.add(get_meeting)
    db.session.commit()
    meeting_schema = MeetingScheme(only=['email','time','venue','host'])
    meeting = meeting_schema.dump(get_meeting)
    return make_response(jsonify({"meeting": meeting}))

@app.route('/api/v1/meeting/<email>',methods=['DELETE'])
def delete_meeting(email):
    get_meeting = Meeting.query.get(email)
    db.session.delete(get_meeting)
    db.session.commit()
    return make_response("", 204)

if __name__ == '__main__':
    app.debug = True    
    app.run()