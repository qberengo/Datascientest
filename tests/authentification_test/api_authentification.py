import os
import requests

# variable d'api
api_adress = '0.0.0.0'
api_port = 5000
api_endpoint = "permissions"
# variable de test
param_user = "Quinlan"
param_psw = 5210
expect_result = "200"

r = requests.post(url='http://{}:{}/{}'.format(api_adress,api_port,api_endpoint), json={'username':'{}'.format(param_user),'password': param_psw})

output = '''
==================================
	Authentication test
==================================

request done at "/{endpoint}"
| username = {user}
| password = {psw}

expected result = {result}
actual result = {status}

=> {test}
'''

status_code = r.status_code
if status_code == int(expect_result):
	test_result = 'SUCCESS'
else: test_result = 'FAILURE'
print(output.format(endpoint=api_endpoint,user=param_user,psw=param_psw,result=expect_result,status=status_code,test=test_result))

if os.environ.get('LOG') == 1:
	with open('api_test.log','a') as file:
		file.write(output)
