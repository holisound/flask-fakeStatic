from flask import Flask, current_app, jsonify


class FakeStatic(object):
    skip_endpoints = {"static", }

    def __init__(self, app=None, skip_endpoints=None):
        if skip_endpoints is not None:
            self.skip_endpoints |= set(skip_endpoints)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for rule in app.url_map.iter_rules():
            if rule.endpoint in self.skip_endpoints:
                continue
            rule.rule += ".html"
            rule.refresh()


app = Flask(__name__)


@app.route("/index")
def index():
    return "index"


@app.route('/routes')
def routes():

    arr = [rule.endpoint for rule in current_app.url_map.iter_rules()]
    return jsonify({"total": len(arr), "data": sorted(arr)})


FakeStatic(app, skip_endpoints=["routes"])
if __name__ == "__main__":
    app.run(debug=True)
