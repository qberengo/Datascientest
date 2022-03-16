import os
import requests

# variable d'api
api_adress = ''
api_port = 8000
api_endpoint = "v1/review"
# variable de test
param_user = "alice"
param_psw = "wonderland"
expect_result = "200"

r = requests.get(url='http://{}:{}/{}'.format(api_adress,api_port,api_endpoint), params={'username':'{}'.format(param_user),'password':'{}'.format(param_psw)})

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