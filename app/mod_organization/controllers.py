from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG

from app.mod_organization.models import App
from app.mod_organization.models import Organization
from app.mod_organization.models import Group
bp_app = Blueprint('app', __name__, url_prefix='/app')
bp_organization = Blueprint('organization', __name__, url_prefix='/organization')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

# Get add page
@bp_organization.route('/add', methods=['GET'])
def add():
    return render_template('organizations.html')

# Get edit page
@bp_organization.route('/edit', methods=['GET'])
def update():
    return render_template('organizations.html')

# Get record by id (return json)
@bp_organization.route('/<int:organizationId>', methods=['GET'])
def get_organization(organizationId):
    organization = Organization.query.filter_by(id=organizationId).first()
    if organization is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify(organization.to_json())

# Get all records
@bp_organization.route('/', methods=['GET'])
def get_organizations():

    organizations = Organization.query.filter_by(archive=False)
    if organizations is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    json_str = json.dumps([c.to_json() for c in organizations])
    return json_str


# Add record
@bp_organization.route('/', methods=['POST'])
def add_organization():

    # Create the object
    name = request.form['name']

    o = Organization(name)

    db.session.add(o)
    db.session.commit()

    return jsonify(o.to_json())

# Update record
@bp_organization.route('/<int:organizationId>', methods=['PUT'])
def update_organization(organizationId):
    o = Organization.query.filter_by(id=organizationId).first()
    if o is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT


    # Create the object
    name = request.form['name']
    o.name = name

    db.session.commit()
    return jsonify(o.to_json())

# Delete the record (archive the record)
@bp_organization.route('/<int:organizationId>', methods=['DELETE'])
def delete_organization(organizationId):

    # Since we never delete data just set
    # the archive flag to true
    o = Organization.query.filter_by(id=organizationId).first()
    if o is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    o.archive = True

    db.session.commit()
    return jsonify(o.to_json())


# Get record by id (return json)
@bp_organization.route('/group/<int:groupId>', methods=['GET'])
def get_group(groupId):
    group = Group.query.filter_by(id=groupId).first()
    if group is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify(group.to_json())

# Get all records
@bp_organization.route('/<int:organizationId>/group', methods=['GET'])
def get_groups(organizationId):

    groups = Group.query.filter_by(organizationId=organizationId).filter_by(archive=False)
    if groups is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    json_str = json.dumps([c.to_json() for c in groups])
    return json_str


# Add record
@bp_organization.route('/<int:organizationId>/group/', methods=['POST'])
def add_group(organizationId):

    # Create the object
    name = request.form['name']

    g = Group(organizationId, name)

    db.session.add(g)
    db.session.commit()

    return jsonify(g.to_json())

# Update record
@bp_organization.route('/group/<int:groupId>', methods=['PUT'])
def update_group(groupId):
    g = Group.query.filter_by(id=groupId).first()
    if g is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT


    # Create the object
    name = request.form['name']
    g.name = name

    db.session.commit()
    return jsonify(g.to_json())

# Delete the record (archive the record)
@bp_organization.route('/group/<int:groupId>', methods=['DELETE'])
def delete_group(groupId):

    # Since we never delete data just set
    # the archive flag to true
    g = Group.query.filter_by(id=groupId).first()
    if g is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    g.archive = True

    db.session.commit()
    return jsonify(g.to_json())


# Get record by id (return json)
@bp_app.route('/<int:appId>', methods=['GET'])
def get_app(appId):
    app = App.query.filter_by(id=appId).first()
    if app is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify(app.to_json())

# Get all records
@bp_app.route('/', methods=['GET'])
def get_apps():

    apps = App.query.filter_by(archive=False)
    if apps is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    json_str = json.dumps([a.to_json() for a in apps])
    return json_str


# Add record
@bp_app.route('/', methods=['POST'])
def add_app():

    # Create the object
    name = request.form['name']

    a = App(name)

    db.session.add(a)
    db.session.commit()

    return jsonify(a.to_json())

# Update record
@bp_app.route('/<int:appId>', methods=['PUT'])
def update_app(appId):
    a = App.query.filter_by(id=appId).first()
    if a is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT


    # Create the object
    name = request.form['name']
    a.name = name

    db.session.commit()
    return jsonify(a.to_json())

# Delete the record (archive the record)
@bp_app.route('/<int:appId>', methods=['DELETE'])
def delete_app(appId):

    # Since we never delete data just set
    # the archive flag to true
    a = App.query.filter_by(id=appId).first()
    if a is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    a.archive = True

    db.session.commit()
    return jsonify(a.to_json())
