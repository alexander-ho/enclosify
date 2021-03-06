import string
import sys
import tornado.ioloop
import tornado.web
from tornado.template import Loader
import logging
import os


try:
    assert sys.version_info >= (3, 0)
except AssertionError:
    sys.exit("This script requires python 3.0 or higher.")


class MainHandler(tornado.web.RequestHandler):
        def output_block(self, letter):
            a_to_j = string.ascii_lowercase[0:10]
            k_to_z = string.ascii_lowercase[10:]
            if letter in a_to_j:
                unicode_prefix = '1F1E'
                position = a_to_j.index(letter)
                # offset by 5 to get the actual value
                value = position + 6
            elif letter in k_to_z:
                unicode_prefix = '1F1F'
                position = k_to_z.index(letter)
                value = position
            else:
                return " "
            # convert number to hex and exclude the 0x
            hex_value = hex(value)[-1]
            unicode_prefix += str(hex_value)
            # this is where the magic happens.
            block_letter = chr(int(unicode_prefix, 16))
            return block_letter

        def get(self):
            web = Loader("./")
            phrase = self.get_argument("enclosify", "").lower()
            if phrase == "":
                phrase = "enclosify text"
            enclosed_text = ""
            for letter in phrase:
                enclosed_text += "{} ".format(self.output_block(letter))
            msg = web.load("enclosify.html").generate(
                            enclosed_text=enclosed_text)
            self.write(msg)
            return


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    application.listen(8889)
    logging.info("Ready to enclosify on port 8889. Hit Ctrl-C to cancel.")
    tornado.ioloop.IOLoop.current().start()
