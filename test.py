import requests

bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NvZGUiOiJhZG1pbmlzdHJhdG9yIiwiZXhwIjoxNzE3NTcyNTAyfQ.euf8dQnQMwqrub6AB_Hb0DBtp7sz_Bt5IOQf0zeImyE"
headers = {"Authorization": f"Bearer {bearer_token}"}

response = requests.get("http://192.168.100.105:8000/commission/K1", headers=headers)

print(response.json())

# print("Hello World")

# @app.route('/postlogin', methods=['POST','GET'])
# def postlogin():
#     username = request.form['username']
#     password = request.form['password']
#     if request.method == "POST":
#         #
#         if username == 'admin' and password == 'password':
#             #
#             session['bearer_token'] = bearer_token
#             return redirect('/api/commissions')
#             # session['next'] = request.args.get('next')
#             # return redirect(url_for('success'))
#     else:
#         return 'Login failed'