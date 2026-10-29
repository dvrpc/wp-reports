from sanic import Blueprint, Sanic

from fy25 import bp as fy25
from fy26 import bp as fy26
from fy27 import bp as fy27
from fy28 import bp as fy28

app = Sanic(__name__)
# Set SANIC_URL_PREFIX env variable
url_prefix = getattr(app.config, "URL_PREFIX", "/wp-reports")

api = Blueprint.group(fy25, fy26, fy27, fy28, url_prefix=url_prefix)
app.blueprint(api)
