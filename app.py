from flask import Flask

# ===== BluePrints =====
from api.delivery_tracker.cj import cj
from api.delivery_tracker.epost import epost
from api.delivery_tracker.logen import logen
from api.delivery_tracker.lotte import lotte
from api.auth import auth

# ===== App Initializing =====
app = Flask(__name__)

# ===== Registering Blueprints =====
app.register_blueprint(cj)
app.register_blueprint(epost)
app.register_blueprint(logen)
app.register_blueprint(lotte)

app.register_blueprint(auth)
