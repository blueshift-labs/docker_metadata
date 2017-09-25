from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
FlaskJSON(app)

import metadata

@app.route('/inspect', methods=['GET'])
@as_json
def inspect_api():
  try:
    docker_id = request.args['id']
    docker_long_id, response = metadata.docker_inspect(docker_id)
    response['EcsMetadata'] =  metadata.ecs_inspect(docker_long_id)
  except Exception as ex:
    raise JsonError(success=False, error=str(ex))
  return json_response(result=response, success=True)

if __name__ == '__main__':
  app.run(debug=False, host='0.0.0.0')

# docker run  -v /var/run/docker.sock:/var/run/docker.sock --net=host -p 5000:5000 -it 30f1816623d7 bash
