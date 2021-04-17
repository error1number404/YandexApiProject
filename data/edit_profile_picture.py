from PIL import Image
def edit_profile_picture(link):
    im = Image.open(link)
    x, y = im.size
    im.resize((150,150)).save(link)