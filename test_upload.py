import urllib.request, io, uuid

boundary = uuid.uuid4().hex
with open('app/services/__init__.py', 'rb') as f:
    file_data = f.read()

body = io.BytesIO()
body.write(b'--' + boundary.encode() + b'\r\n')
body.write(b'Content-Disposition: form-data; name="file"; filename="test.py"\r\n')
body.write(b'Content-Type: application/octet-stream\r\n\r\n')
body.write(file_data)
body.write(b'\r\n')
body.write(b'--' + boundary.encode() + b'\r\n')
body.write(b'Content-Disposition: form-data; name="project_name"\r\n\r\n')
body.write(b'test\r\n')
body.write(b'--' + boundary.encode() + b'\r\n')
body.write(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
body.write(b'test\r\n')
body.write(b'--' + boundary.encode() + b'--\r\n')

req = urllib.request.Request(
    'http://localhost/api/v1/upload/source',
    data=body.getvalue(),
    headers={'Content-Type': 'multipart/form-data; boundary=' + boundary}
)
try:
    resp = urllib.request.urlopen(req)
    print('Status:', resp.status)
    print('Body:', resp.read().decode())
except urllib.error.HTTPError as e:
    print('Status:', e.code)
    print('Body:', e.read().decode())
