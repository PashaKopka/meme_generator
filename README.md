# Meme Generator

This package add text on image and send it through telegram using python.\
Thanks for checking it out.

## Getting started

You must to write config for your bot:
```
[pyrogram]
api_id = _your telegram id_
api_hash = _your telegram hash_

[imgur]
id = _your imgur id_
secret = _your imgur secret_
```

To get this data you must to login on this urls:
 - [telegram](https://my.telegram.org/auth)
 - [imgur](https://api.imgur.com/oauth2/addclient)

Install requirenments.txt:
```bash
pip install -r requirenments.txt
```
Then put your img to directory with _main.py_
```python
TelegramUserBot('img.jpg', cordinates=(100, 72))
```
edit data in class initialising 
