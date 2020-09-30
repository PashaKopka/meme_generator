import cv2
from pyrogram import Client, filters
import test
import os
from imgurpython import ImgurClient

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


class ImgMaker:

    def __init__(self, input_img, text, font=cv2.FONT_HERSHEY_COMPLEX, text_color=(0, 0, 0)):
        self.input_img = cv2.imread(input_img)
        self.text = text
        self.text_font = font
        self.text_color = text_color
        self.output_img = 'img.png'

    def make_img(self):
        cv2.putText(self.input_img, self.text, (100, 72), self.text_font, 1, color=self.text_color, thickness=2)
        cv2.imwrite(self.output_img, self.input_img)
        return self.output_img


class ConfigParserFacade:

    def __init__(self, config_path="config.ini"):
        self.client_id = os.environ.get("IMGUR_API_ID")
        self.client_secret = os.environ.get("IMGUR_API_SECRET")
        self.refresh_token = os.environ.get("IMGUR_REFRESH_TOKEN")
        self.config_parser = ConfigParser.SafeConfigParser()
        self.config_path = config_path

    def get_config(self):
        self.config_parser.read(self.config_path)

        imgur = dict(self.config_parser.items("imgur"))

        client_id = self.client_id or imgur.get("id")
        client_secret = self.client_secret or imgur.get("secret")
        refresh_token = self.refresh_token or imgur.get("refresh_token", "")

        if not (client_id and client_secret):
            raise (
                "Cannot upload - could not find IMGUR_API_ID or "
                "IMGUR_API_SECRET environment variables or config file"
            )

        data = {"id": client_id, "secret": client_secret}
        if refresh_token:
            data["refresh_token"] = refresh_token
        return data


class UploaderImgToImgur:

    def __init__(self, input_img, text):
        self.config_parser = ConfigParserFacade()
        self.img_maker = ImgMaker(input_img, text)

    def upload_img(self):
        config = self.config_parser.get_config()
        img = self.img_maker.make_img()
        if "refresh_token" in config:
            client = ImgurClient(config["id"], config["secret"], refresh_token=config["refresh_token"])
            anon = False
        else:
            client = ImgurClient(config["id"], config["secret"])
            anon = True

        response = client.upload_from_path(img, anon=anon)
        return response["link"]


upl = UploaderImgToImgur('img.jpg', 'test')
print(upl.upload_img())


class TelegramUserBot:

    def __init__(self, input_img):
        app = Client('my_user_bot')

        @app.on_message(filters.command("meme", prefixes=".") & filters.me)
        def send_img(app, message):
            message.delete()
            text = message.text.split(".meme ", maxsplit=1)[1]
            img_uploader = UploaderImgToImgur(input_img, text)
            link = img_uploader.upload_img()

            app.send_photo(message['chat']['username'], photo=link)

        app.run()

# @app.on_message(filters.command("meme", prefixes=".") & filters.me)
# def type(app, message):
#     message.delete()
#     text = message.text.split(".meme ", maxsplit=1)[1]
#     test.make_img(text)
#     link = upload_image('img.png')
#     app.send_photo(message['chat']['username'], photo=link)


TelegramUserBot('img.jpg')
