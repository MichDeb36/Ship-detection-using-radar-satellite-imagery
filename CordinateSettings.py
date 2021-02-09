import gdal
from SearchShips import FindShips
from GlobalContener import ShipContainer

class CoordinateSettings():
    TIFF_PATH = "data/images_tiff/"     # folder gdzie są obrazy w formacie .tiff
    TXT_PATH = "data/info_txt/"  # folder gdzie będą się zapisywać pliki txt z informacjami
    finder = FindShips()

    # ustawieniae getransformacji
    def settinGeotransformation(self, file):
        file = file.split('.')[0] + '.tiff'
        fn = self.TIFF_PATH + file
        ds = gdal.Open(fn, gdal.GA_Update)
        gcps = ds.GetGCPs()
        gt = gdal.GCPsToGeoTransform(gcps)
        return gt

    def imageProcessing(self,x1, y1, x2, y2, x3, y3, x4, y4, tiffFile, pngFile):
        gt = self.settinGeotransformation(tiffFile)  # ustawienie getrasnformacji
        cornerX = x1
        cornerY = y1
        x1, y1 = self.pixel2coord2(x1, y1, gt)
        x2, y2 = self.pixel2coord2(x2, y2, gt)
        x3, y3 = self.pixel2coord2(x3, y3, gt)
        x4, y4 = self.pixel2coord2(x4, y4, gt)

        self.saveCornersSmallImages(pngFile, x1, y1, x2, y2, x3, y3, x4, y4, cornerX, cornerY)
        self.findCoordinates(pngFile, gt)


    # zapisanie wspolrzednych rogow malych zdjec oraz ich pikseli
    def saveCornersSmallImages(self, file, x1, y1, x2, y2, x3, y3, x4, y4, cornerX, cornerY):
        outfile = file.split('.')[0] + 'corners.txt'
        f = open(self.TXT_PATH + outfile, "w")
        # piksele glownego rogu
        f.write(str(cornerX) + '\n')
        f.write(str(cornerY) + '\n')
        # wspolrzedne rogow
        f.write(str(x1) + '\n')
        f.write(str(y1) + '\n')
        f.write(str(x2) + '\n')
        f.write(str(y2) + '\n')
        f.write(str(x3) + '\n')
        f.write(str(y3) + '\n')
        f.write(str(x4) + '\n')
        f.write(str(y4) + '\n')
        f.close()
        print('save: ' + outfile)

    # wyszukiwanie stakow z uzyciem yolo
    def findCoordinates(self, nameFile, gt):
        contener = ShipContainer()
        ships = self.finder.searchImages(nameFile)
        counter = 0
        for s in ships:
            a, b = s
            x, y = self.pixel2coord2(int(a), int(b), gt)    # sprawdznie wspolrzednych znalezonych statkow
            contener.setGlobalShips(x, y)                   # wpisanie wsplrzednych do globalnej tablicy
            counter += 1
        contener.createGlobalShipsTxt(nameFile)


    # zamiana pikseli na wspolrzedne
    def pixel2coord2(self, col, row, gt):
        """Returns global coordinates to pixel center using base-0 raster index"""
        c, a, b, f, d, e = gt
        xp = a * col + b * row + a * 0.5 + b * 0.5 + c
        yp = d * col + e * row + d * 0.5 + e * 0.5 + f
        return (xp, yp)

