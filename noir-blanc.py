from PIL import Image
img = Image.open("pomme.jpg")
def calculmoyenne(img):
    largeur,hauteur=img.size
    s_r,s_v,s_b=0,0,0
    for y in range(hauteur):
        for x in range(largeur):
            r,v,b=img.getpixel((x,y))
            s_r=s_r+r
            s_v=s_v+v
            s_b=s_b+b
    return (s_r+s_v+s_b)/(largeur*hauteur)

m=calculmoyenne(img)
largeur,hauteur=img.size
for y in range(hauteur):
    for x in range(largeur):
        r,v,b=img.getpixel((x,y))
        if r+v+b>m:
            img.putpixel((x,y),(255,255,255))
        else:
            img.putpixel((x,y),(0,0,0))
img.show()