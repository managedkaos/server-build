from flask import Flask
from flask import request
from flask import jsonify, make_response
import json
import subprocess

micro = Flask(__name__)

@micro.route("/hello", methods=['GET'])
def hello():
    process = subprocess.Popen(['/usr/bin/Rscript', '/opt/microservice/hello.r'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
    out, err = process.communicate()
    return make_response(jsonify({'out':out.decode("utf-8") , 'err':err.decode("utf-8") }), 200)

@micro.route("/", methods=['GET', 'POST'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        r = requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        print(js['Message'])

        message = json.loads(js['Message'])
        bucket  = message['Records'][0]['s3']['bucket']['name']
        key     = message['Records'][0]['s3']['object']['key']

        print(f'Bucket {bucket}')
        print(f'Key    {key}')

        # CALL R FUNCTION HERE WITH BUCKET AND KEY

        return make_response('Notification Processed', 200)

    return make_response('OK', 200)

if __name__ == "__main__" :
    micro.run()

