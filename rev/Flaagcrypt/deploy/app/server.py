from flask import Flask, request

flag = "nnctf{L4_cl4v3_s13mpRe_eStUvOO_aqUIII!!11!1}"

flag_fake = "nonoceteefe{n0_fL4g_4_u_<3}"

ret_flag = ""

for char in flag:
    ret_flag += chr(ord(char) ^ 0x0A)

ret_flag_fake = ""

for char in flag_fake:
    ret_flag_fake += chr(ord(char) ^ 0x0A)

app = Flask("server")

@app.route("/asdow90qwmfuisd", methods=["GET"])
def get_flag():
    print(request.headers)
    print(request.user_agent.string)
    
    if request.headers.get("Xx-Skibidi-Xx") == "Mira mama, estoy en la tele" and request.user_agent.string == "":
        return ret_flag
    
    else:
        return ret_flag_fake
    
if __name__ == "__main__":
    app.run("0.0.0.0", 5000)