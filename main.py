
from PIL import Image


class noeud:

    def __init__(self, image, cadre,prof):
        self.cadre = cadre  # tuple avec les coordonnées du cadre du noeud
        self.fils = []  # a des fils si pas une image unicolore
        self.img = image  # recadrage de l'image du noeud
        self.val=0
        self.prof=prof
    def cadre(self):
        return self.cadre
    def val(self):
        return self.val
    def prof(self):
        return self.prof
    def division(self):
        left, top, L, H = self.cadre  # coordonnées point haut gauche et point bas droit
        # coordonnées absolues
        Largeur = int((L - left) / 2)
        Hauteur = int((H - top) / 2)
        mil_x = left + Largeur  # milieu vertical du cadre
        mil_y = top + Hauteur  # milieu horizontal du cadre

        gh = noeud(self.img.crop((0, 0, Largeur, Hauteur)), (left, top, mil_x, mil_y),self.prof+1)  # fils nw
        dh = noeud(self.img.crop((Largeur, 0, 2 * Largeur, Hauteur)), (mil_x, top, L, mil_y),self.prof+1)  # fils ne
        gb = noeud(self.img.crop((0, Hauteur, Largeur, 2 * Hauteur)), (left, mil_y, mil_x, H),self.prof+1)  # fils sw
        db = noeud(self.img.crop((Largeur, Hauteur, 2 * Largeur, 2 * Hauteur)), (mil_x, mil_y, L, H),self.prof+1)  # fils se
        self.fils = [gh, dh, gb, db]  # liste des fils

    def color(self):
        """
        retourne 0 si blanc 1 si noir et 2 si ni noir ni blanc (mélange de pixels noirs et blancs)
        """
        colors = [(255, 255, 255), (0, 0, 0)]
        L, H = self.img.size
        prempix = self.img.getpixel((0, 0))[0:3]
        for i in range(0, L):
            for j in range(0, H):
                if self.img.getpixel((i, j))[0:3] != prempix:
                    return 2
        return colors.index(prempix)  # retourne l'index de la couleur dans le tableau colors.


# Pour le quadtree, on choisit de le représenter avec une liste à 4 éléments : si le cadran est blanc on met un 0, si le cadran est noir un 1, sinon, une autre liste à 4 éléments.
# Attention si l'image est complètement blanche ou noire à la base, on renverra 0 ou 1, qui n'est pas une liste.
# si tu veux reconstruire ton image, tu auras éventuellement à modifier le type du quadtree.

def build_quadtree(noeud):  # construit l'arbre à partir d'une image, en divisant le noeud inséré en quatre récursivement, si ce n'est pas une feuille
    x, y, L, H = noeud.cadre
    couleur = noeud.color()
    if couleur == 0:
        noeud.val=0
        return [noeud.cadre, noeud.val,noeud.prof]
    elif couleur == 1:
        noeud.val=1
        return [noeud.cadre, noeud.val,noeud.prof]
    else:
        cadr=noeud.cadre
        noeud.division()
        return [build_quadtree(fils) for fils in noeud.fils]+[cadr] #  cadr --> cadre du noeud pére
#à partir de l'ENORME liste renvoyé par la fonction build_quadtree on va pouvoir construire l'image compressé

def build_quadtreeimg(L,profondeur,image):              #construit l'image compressé selon le niveau de profondeur
    clr=[(255,255,255),(0,0,0)]
    img=image
    pf=profondeur
    for O in range (len(L)-1):
        pf-=1
        if testlst(L[O]) :                              #permet de savoir si c'est une feuille ou pas
            if pf<=0:
                cdr=L[O][4]                             #renvoie au cadre du bloc de pixel (j'ai rajouté à chaque liste de fils un 5 elts qui est un tuple représentant le cadre du noeud pére)
                for i in range(cdr[0],int((cdr[2]+1))):
                    for j in range(cdr[1],int((cdr[3]+1))):
                        img.putpixel((i,j),(128,128,128))
            else:
                build_quadtreeimg(L[O],pf,image)        #descends au niveau de profondeur suivant
        else:  # le noeud est une feuille
            cd=L[O][0]
            for i in range(cd[0],cd[2]+1):                 #rajoute le bloc de pixels noir ou blanc

                for j in range(cd[1], cd[3]+1):
                    img.putpixel((i,j),clr[L[O][1]])
    return img



def testlst(L):                                 #vérifie si c'est une liste, le is list ne marchait pas, peut être parcequ'il y'avait trop d'info
    txt=str(L)
    n=0
    for elt in txt:
        if elt =="[":
            n+=1
    return n>1



def unbuild_quadtree(noeud):
    pass




image = Image.open("pomme_nb.png")



image.show()

Noeud = noeud(image, (0, 0, *image.size),0)
L=build_quadtree(Noeud)
print(L)
images=Image.new("RGB",(513,513)) #nouveau support
img=build_quadtreeimg(L,15,images)

img.show()

# si checkez les infos de l'image vous allez remarquer que la taille diminue de moitier bien sur selon le niveau de profondeur


