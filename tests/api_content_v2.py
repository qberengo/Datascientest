import os
import requests

# variable d'api
api_adress = 'api'
api_port = 8000
api_endpoint = "v2/review"
# variable de test
param_user = "alice"
param_psw = "wonderland"
param_sent = "life is beautiful"
expect_result = "positif"

r = requests.get(url='http://{}:{}/{}'.format(api_adress,api_port,api_endpoint), params={'username':'{}'.format(param_user),'password':'{}'.format(param_psw),'sentence':'{}'.format(param_sent)})

output = '''
==================================
	    Content test
==================================

request done at "/{endpoint}"
| username = {user}
| password = {psw}
| sentence = {sentence}

expected result = {result}
actual result = {status}

=> {test}
'''

status_code = r.json()['score']
if expect_result == "positif":
	if status_code > 0:
		test_result = 'SUCCESS'
	else: test_result = 'FAILURE'
else:
	if status_code < 0:
		test_result = 'SUCCESS'
	else: test_result = 'FAILURE'
print(output.format(endpoint=api_endpoint,user=param_user,psw=param_psw,result=expect_result,status=status_code,test=test_result,sentence=param_sent))

if os.environ.get('LOG') == 1:
	with open('api_test.log','a') as file:
		file.write(output)