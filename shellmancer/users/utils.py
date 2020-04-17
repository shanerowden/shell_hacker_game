import os
import secrets
from PIL import Image

from shellmancer import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/img/pfp', picture_fn)

    # resize
    basewidth = 128
    img = Image.open(form_picture)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))

    img.save(picture_path)
    return picture_fn
