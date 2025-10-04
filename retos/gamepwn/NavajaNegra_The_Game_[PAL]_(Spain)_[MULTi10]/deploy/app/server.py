from flask import Flask

flag = "nnctf{3nC0ntr4St3_lA_eSc4L3r444!!!__Gr4NdeEE33}"

app = Flask(
    "flag"
)

@app.route("/")
def get_flag():
    return flag

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
