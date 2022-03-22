from PIL import Image

def resizeIMG(imgpath,outputpath):
    output_size = (512,512)
    i = Image.open(imgpath)
    i.thumbnail(output_size)
    i.save(outputpath)
    
resizeIMG("trial01.gif","001-trial01.gif")
