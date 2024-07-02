# simple-token-implement

# Overview
This API allows clients to request tokens. Each token represents a permission or a right to perform certain actions within another service. The total number of tokens available is configurable through an environment variable.

Based on the provided Python script snippet and previous context about the [`simple-token-implement.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fwzh%2Fdev%2Fsimple-token-implement%2Fsimple-token-implement.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/wzh/dev/simple-token-implement/simple-token-implement.py") application, here's a simple API documentation in Markdown format. This documentation assumes the application provides an endpoint to issue tokens and requires a password sent as a header for authorization.

---

# Simple Token Implement API Documentation

## Overview

This API allows clients to request tokens. Each token represents a permission or a right to perform certain actions within another service. The total number of tokens available is configurable through an environment variable.

## Authentication

Requests to this API must include an `X-API-PASSWORD` header with the correct password.

## API Endpoints

### Issue Token

- **URL**: `/issue_token`
- **Method**: `GET`
- **Auth Required**: Yes
- **Headers**:
  - `X-API-PASSWORD`: The password for accessing the API.
- **URL Params**: 
  - `info`: Optional. Additional information or context for the token request.
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: 
    ```json
    {
      "message": "Token issued successfully.",
      "available_tokens": [number of available tokens after issuing],
      "info": [echoed info parameter if provided]
    }
    ```
- **Error Response**:
  - **Code**: 401 Unauthorized
  - **Content**:
    ```json
    {
      "error": "Unauthorized"
    }
    ```
  - **Condition**: If the `X-API-PASSWORD` header is missing or incorrect.
  - **Code**: 429 Too Many Requests
  - **Content**:
    ```json
    {
      "message": "No tokens available.",
      "available_tokens": 0,
      "info": [echoed info parameter if provided]
    }
    ```
  - **Condition**: If there are no tokens available to be issued.

## Examples

### Requesting a Token

```bash


curl

 -H "X-API-PASSWORD: your_password_here" "http://localhost:5000/issue_token?info=example"
```

### Response

```json
{
  "message": "Token issued successfully.",
  "available_tokens": 9,
  "info": "example"
}
```


# end

```bash

# on host to test
pip install -U flask jsonify Lock 

# build container
cd /data

git clone https://github.com/wangzheng422/simple-token-implement

cd simple-token-implement

podman build -t quay.io/wangzheng422/qimgs:simple-token-implement-2024.07.02-v01 -f py311.dockerfile ./

podman push quay.io/wangzheng422/qimgs:simple-token-implement-2024.07.02-v01

# try it
podman run -p 5000:5000 \
    -e TOTAL_TOKENS=1 \
    -e TIMER_DURATION=10 \
    quay.io/wangzheng422/qimgs:simple-token-implement-2024.07.02-v01

# make api call
curl -H "X-API-PASSWORD: your_password_here" http://localhost:5000/issue_token

```