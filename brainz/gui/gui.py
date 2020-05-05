from flask import Flask, render_template


def run_server(host: str, port: int, api_host: str, api_port: int):
    """
    Run the gui server using the given api server.

    :param host: The gui-server's host.
    :param port: The gui-server's port.
    :param api_host: The api-server's host.
    :param api_port: The api-server's port.
    """
    app = get_app(api_host, api_port)
    app.run(host=host, port=port)


def get_app(api_host: str, api_port: int):
    """
    Get the gui-server's flask app.
    """
    app = Flask(__name__, static_folder="build/static", template_folder="build")

    @app.route("/")
    def index():
        return render_template("index.html", api_server=f"http://{api_host}:{api_port}")

    return app
