import requests



response = requests.get("http://127.0.0.1:8001/")
data = response.json()
print("File Server dir: ", data['files'])

post_msg = {'file_name': 'posted_file1', 'content': 'This is content that goes into a written file.'}
# Create a file
response = requests.post('http://localhost:8001/', json=post_msg)

response = requests.get("http://127.0.0.1:8001/")
data = response.json()
print("File Server dir: ", data['files'])

