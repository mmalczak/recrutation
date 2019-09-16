import requests
s = requests.Session()
r = s.put('http://20.0.0.2:8080/', data={'value':'12'})
print(r.text)
r = s.get('http://20.0.0.2:8080/')
print(r.text)
