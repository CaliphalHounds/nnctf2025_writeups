from flask import Flask, render_template, request, g, jsonify, make_response
import jwt
import secrets
import os

app = Flask(__name__)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

FLAG = os.getenv("FLAG")


@app.before_request
def jwt_cookie_middleware():
    g.miguelitoCoin = None
    g.nocheNNCoin = None
    g.navajaCoin = None
    g.token = None

    token = request.cookies.get("auth_token")

    if not token:
        return

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        g.miguelitoCoin = payload.get("miguelitoCoin")
        g.nocheNNCoin = payload.get("nocheNNCoin")
        g.navajaCoin = payload.get("navajaCoin")

        g.token = token

    except jwt.ExpiredSignatureError:
        # Token expired
        app.logger.warning("JWT expired")
    except jwt.InvalidTokenError:
        # Token invalid
        app.logger.warning("Invalid JWT token")


@app.route("/get-values")
def get_values():
    return jsonify(
        {
            "miguelitoCoin": g.miguelitoCoin,
            "nocheNNCoin": g.nocheNNCoin,
            "navajaCoin": g.navajaCoin,
        }
    )


@app.route("/")
def coins_page():
    resp = make_response(render_template("coins.html", app_name="NavajaWallet"))


    # Balance inicial para que el usuario disfrute de NavajaWallet
    if g.token is None:

        payload = {"miguelitoCoin": 0.0, "nocheNNCoin": 0.0, "navajaCoin": 10.0}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        resp.set_cookie("auth_token", token, httponly=True, samesite="Lax")

    return resp


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.json
    source = data.get("source")
    target = data.get("target")
    amount = float(data.get("amount", 0))

    balances = {
        "miguelitoCoin": g.miguelitoCoin,
        "nocheNNCoin": g.nocheNNCoin,
        "navajaCoin": g.navajaCoin,
    }

    if source not in balances or target not in balances:
        return jsonify({"error": "Coin inválida"}), 400
    if source == target:
        return jsonify({"error": "Source y target deben ser diferentes"}), 400
    if balances[source] < amount:
        return jsonify({"error": "Insuficientes fondos"}), 400

    balances[source] -= amount
    balances[target] += amount

    token = jwt.encode(balances, JWT_SECRET, algorithm=JWT_ALGORITHM)

    resp = make_response(jsonify(balances))
    resp.set_cookie("auth_token", token, httponly=True, samesite="Lax")
    return resp


@app.route("/flag")
def get_flag():

    if g.token is None:
        return jsonify({"message": "No se ha proporcionado token"})

    balances = {
        "miguelitoCoin": g.miguelitoCoin,
        "nocheNNCoin": g.nocheNNCoin,
        "navajaCoin": g.navajaCoin,
    }

    # Obviamente solo los que mas inviertan en NavajaWallet pueden obtener la FLAG

    if all(value > 1000000 for value in balances.values()):
        return jsonify({"flag": FLAG})

    return jsonify({"message": "Balances de cuente insuficientes"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
