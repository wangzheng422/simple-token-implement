# simple-token-implement

# Overview

This API allows clients to request tokens. Each token represents a permission or a right to perform certain actions within another service. The total number of tokens available is configurable through an environment variable. Currently, it is better to use only 1 token, as token timeout case is not implemented for several tokens.

For the token, it has such logic:
1. issue a token
2. release/recycle the token
3. token has a pre-defined timeout, for case such as pod restart, and the token is not released properly. If token timeout is reached, it is automatically released.

This documentation assumes the application provides an endpoint to issue tokens and requires a password sent as a header for authorization.

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
curl -H "X-API-PASSWORD: your_password_here" "http://localhost:5000/issue_token?info=example"
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