# mini-wallet-exercise

A simple API using django-rest-framework and sqlite. Made using Python 3.8.

Installation:

```
git clone https://github.com/satryopramahardi/mini-wallet-exercise.git
python -m venv env
source venv/bin/activate
pip install -r requirements.txt
```

How to run:
```
cd miniwallet
python manage.py runserver
```

The app should be running on `http://127.0.0.1:8000/`. You can find the API url in `http://127.0.0.1:8000/api/v1/`
There are 4 endpoints on this mini project:
```
http://127.0.0.1:8000/api/v1/init
http://127.0.0.1:8000/api/v1/wallet
http://127.0.0.1:8000/api/v1/wallet/deposits
http://127.0.0.1:8000/api/v1/wallet/withdrawals
```

### `http://127.0.0.1:8000/api/v1/init`
Request:
```
curl --location --request POST 'http://localhost/api/v1/wallet' \
--form 'customer_xid="ea0212d3-abd6-406f-8c67-868e814a2436"'
```
customer_xid have to be 36 characters. Each customer will get 1 wallet and 1 token.

Will respond token for authorization

### `http://127.0.0.1:8000/api/v1/wallet`
Requested by using authorization token:
```
--header 'Authorization: Token 6b3f7dc70abexxxxxe56658b86fa50xxxxxxxxxx'
```
You can get the token from `/init`. Utilizes `GET` to check wallet, `POST` to enable wallet, and `PATCH` to disable wallet.

### `http://127.0.0.1:8000/api/v1/wallet/deposits`
Requested using the same token with request parameter:
```
amount: amount you want to deposit
reference_id: id for each transaction (must be 36 char)
```
You wont be able to change your amount if you disable your wallet. Reference_id have to be unique. Using `POST` method.

### `http://127.0.0.1:8000/api/v1/wallet/withdrawals`
Requested using the same token with request parameter:
```
amount: amount you want to withdraw
reference_id: id for each transaction(must be 36 char)
```
You wont be able to change your amount if you disable your wallet. Can't withdraw exeeding the balance amount. Using `POST` method.
