from flask import Flask
import subprocess

micro = Flask(__name__)

@micro.route("/hello")
def hello():
    process = subprocess.Popen(['/usr/bin/Rscript', '/opt/microservice/hello.r'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
    out, err = process.communicate()
    print(out)
    print(err)
    return out

if __name__ == "__main__" :
    micro.run()
