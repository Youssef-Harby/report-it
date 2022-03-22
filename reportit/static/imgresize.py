from PIL import Image

def resizeIMG(imgpath,outputpath):
    output_size = (512,512)
    i = Image.open(imgpath)
    i.thumbnail(output_size)
    i.save(outputpath)
    
resizeIMG("HS3.png","001-HS3.png")
