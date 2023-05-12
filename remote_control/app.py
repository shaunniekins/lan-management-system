import io
from flask import Flask, Response, request, jsonify, render_template
from utils.db_connection import get_database

try:
  from werkzeug.wsgi import FileWrapper
except Exception as e:
  from werkzeug import FileWrapper


db = get_database()
cursor = db.cursor()
query = "SELECT user_id FROM `active_user_ip` WHERE user_type='student' AND is_active=1;"
cursor.execute(query, )



global STATE
STATE = {}

app = Flask(__name__)

''' Client '''

@app.route('/')
def root():
  return render_template('/index.html')

@app.route('/rd', methods=['POST'])
def rd():
  req = request.get_json()
  key = req['_key']

  if req['filename'] == STATE[key]['filename']:
    attachment = io.BytesIO(b'')
  else:
    attachment = io.BytesIO(STATE[key]['im'])

  w = FileWrapper(attachment)
  resp = Response(w, mimetype='text/plain', direct_passthrough=True)
  resp.headers['filename'] = STATE[key]['filename']
  
  return resp

@app.route('/event_post', methods=['POST'])
def event_post():
    global STATE

    db = get_database()
    cursor = db.cursor()
    query = "SELECT user_id FROM `active_user_ip` WHERE user_type='student' AND is_active=1;"
    cursor.execute(query)

    # Use fetchall() to get all the rows returned by the query
    rows = cursor.fetchall()

    # Convert the rows into a list of user_ids
    user_ids = [row[0] for row in rows]
    
    print("user_ids", user_ids)

    # Assign the user_ids as the keys in the STATE dictionary
    for user_id in user_ids:
        STATE[user_id] = {
            'im': b'',
            'filename': '',
            'events': []
        }

    req = request.get_json()
    key = req['_key']

    STATE[key]['events'].append(request.get_json())
    return jsonify({'ok': True})



''' Remote '''

@app.route('/new_session', methods=['POST'])
def new_session():
  global STATE

  req = request.get_json()
  key = req['_key']
  STATE[key] = {
    'im': b'',
    'filename': 'none.png',
    'events': []
  }

  return jsonify({'ok': True})

@app.route('/capture_post', methods=['POST'])
def capture_post():
  global STATE
  
  with io.BytesIO() as image_data:
    filename = list(request.files.keys())[0]
    key = filename.split('_')[1]
    request.files[filename].save(image_data)
    STATE[key]['im'] = image_data.getvalue()
    STATE[key]['filename'] = filename

  return jsonify({'ok': True})

@app.route('/events_get', methods=['POST'])
def events_get():
  req = request.get_json()
  key = req['_key']
  events_to_execute = STATE[key]['events'].copy()
  STATE[key]['events'] = []
  return jsonify({'events': events_to_execute})


if __name__ == '__main__':
  #app.run('0.0.0.0', debug=True)
  app.run('0.0.0.0')
