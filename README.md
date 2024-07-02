# simple-token-implement


```bash

# on host to test
pip install -U flask jsonify Lock 

# build container
cd /data

git clone https://github.com/wangzheng422/simple-token-implement

cd simple-token-implement

podman build -t quay.io/wangzheng422/qimgs:simple-token-implement-2024.07.02-v01 -f py311.dockerfile ./

# try it
podman run -p 5000:5000 quay.io/wangzheng422/qimgs:simple-token-implement-2024.07.02-v01

# make api call
curl -H "X-API-PASSWORD: your_password_here" http://localhost:5000/issue_token

```