from PIL import Image, ImageOps
import PIL.Image
import os
from CordinateSettings import CoordinateSettings
from DeterminationStartingPoints import DeterminationStartingPoints


class PreparationAndProcessingImages():
    FACTOR_RESOLUTION = 1               #określa o ile podzielimy wysokość i szerokość zdjecia
                                        #jeśli jest ustawiony na 2 to zdjęcie zmniejszy się 4 razy
    PIL.Image.MAX_IMAGE_PIXELS = None   #usuwa ograniczenie maksymalnej ilości pikseli jaki może mieć obraz
    cutImage = True                     #czy zdjecia mają być dzielone na części
    checkSearchShips = True
    ROW = 3                             #ilosc wierszy do podzielenia zdjęcia
    COLUMNS = 6                         #ilosc kolumn do podzielenia zdjecia

    TIFF_PATH = "data/images_tiff/"     # folder gdzie są obrazy w formacie .tiff
    PNG_PATH = "data/images_png/"       # folder gdzie będą się zapisywać obrazy w formacie .png
    TO_LEARN_PATH = "data/learn/"       # folder gdzie będą się zapisywać pociete zdjecia do nauki
    TXT_PATH = "data/info_txt/"         # folder gdzie będą się zapisywać pliki txt z informacjami



    def __init__(self):
        self.convertTiffToPng()


    #konwersja zdjecia z 16bit tiff na 8bit png
    def convertTiffToPng(self):
        for infile in os.listdir(self.TIFF_PATH):                    #pętla pobiera nazwy zdjęć z początkowego folderu
            image = Image.open(self.TIFF_PATH + infile)              #otwieramy zdjęcie w tiff
            print("open : " + infile)
            image = image.convert("L")                               #konwertujemy z 16bit na 8bit skalę szarości
            new_width = int(image.width/self.FACTOR_RESOLUTION)      #dzielimy szerokość zdjecia o FACTOR_RESOLUTION
            new_height = int(image.height/self.FACTOR_RESOLUTION)    #dzielimy wysokosc zdjecia o FACTOR_RESOLUTION
            new_image = image.resize((new_width, new_height))        #ustawiamy nową rodzielczość zjdecia
            outfile = infile.split('.')[0] + '.png'                  #zmieniamy typ obraz na png
            new_image.save(self.PNG_PATH + outfile)                  #zapisujemy nowy obraz (automatyczna konwersja na png)
            image.close()
            print("save : " + outfile)
            if self.cutImage:                                        #sprawdzenie czy tniemy zjęcia
                self.preparationSmallImages(outfile)                 #funkcja do cięcia zdjęć


    def preparationSmallImages(self,infile):
        setCoord = CoordinateSettings()
        startPoints = DeterminationStartingPoints()
        x, y = startPoints.writeGdalInfoDate(infile)                #pobieramy wspolrzedne calego zdjecia (x i y jest ze soba zamienione)
        if(y[0] < y[1]):                                            #sprawdzamy czy musimy przekrecic zdjecie
            self.flipImage(infile)                                  #rotacja zdjecia png
        image = Image.open(self.PNG_PATH + infile)
        print("cutting : " + infile)
        width_small_image = int(image.width/self.COLUMNS)
        height_small_image = int(image.height / self.ROW)
        counter = 1
        for i in range(self.ROW):
            for j in range(self.COLUMNS):
                x1 = 0 + (width_small_image * j)
                y1 = 0 + (height_small_image * i)
                x2 = width_small_image + (width_small_image * j)
                y2 = 0 + (height_small_image * i)
                x3 = 0 + (width_small_image * j)
                y3 = height_small_image + (height_small_image * i)
                x4 = width_small_image + (width_small_image * j)
                y4 = height_small_image + (height_small_image * i)
                image_small = (x1, y1, x4, y4)
                new_img = image.crop(image_small)
                outfile = infile.split('.')[0] +'_'+str(counter)+ '.png'
                new_img.save(self.TO_LEARN_PATH + outfile)
                counter += 1
                print("save : " + outfile)
                if self.checkSearchShips:
                    setCoord.imageProcessing(x1, y1, x2, y2, x3, y3, x4, y4, infile, outfile)


    #obracanie zdjec PNG o 180 stopni
    def flipImage(self,file):
        image = Image.open(self.PNG_PATH + file)
        flipImage = ImageOps.flip(image)
        mirrorImage = ImageOps.mirror(flipImage)
        print("Flip: " + file)
        mirrorImage.save(self.PNG_PATH + file)
        image.close()
        print("Save flip: " + file)


con = PreparationAndProcessingImages()
