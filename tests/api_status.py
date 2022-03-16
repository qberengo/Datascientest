import os
import requests

# variable d'api
api_adress = 'api'
api_port = 8000
api_endpoint = "status"
# variable de test
param_user = ""
param_psw = ""
expect_result = "200"

r = requests.get(url='http://{}:{}/{}'.format(api_adress,api_port,api_endpoint))#, params={'username':'{}'.format(param_user),'password':'{}'.format(param_psw)})

output = '''
==================================
	      Status test
==================================

request done at "/{endpoint}"

expected result = {result}
actual result = {status}

=> {test}
'''

status_code = r.status_code
if status_code == int(expect_result):
	test_result = 'SUCCESS'
else: test_result = 'FAILURE'
print(output.format(endpoint=api_endpoint,result=expect_result,status=status_code,test=test_result))

if os.environ.get('LOG') == 1:
	with open('api_test.log','a') as file:
		file.write(output)