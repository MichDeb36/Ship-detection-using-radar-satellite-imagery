import os
import gdal

class DeterminationStartingPoints():

    TIFF_PATH = "data/images_tiff/"  # folder gdzie są obrazy w formacie .tiff
    TXT_PATH = "data/info_txt/"  # folder gdzie będą się zapisywać pliki txt z informacjami

    # caly gdal info do pliku
    def writeGdalInfoDate(self, file):
        file = file.split('.')[0] + '.tiff'
        var = os.popen('gdalinfo ' + self.TIFF_PATH + file).read()
        fn = self.TIFF_PATH + file
        ds = gdal.Open(fn, gdal.GA_Update)
        outfile = file.split('.')[0] + '.txt'
        f = open(self.TXT_PATH + outfile, "w")
        f.write(var)
        f.close()

        sizeY = ds.RasterYSize - 1
        sizeX = ds.RasterXSize - 1

        """ Znajdz w pliku linie zawierajace danego stringa """

        x = []
        y = []
        myLine = self.checkIfStringInFile(outfile, "(0,0)")
        x, y = self.convertLineToFloat(myLine, x, y)

        myLine = self.checkIfStringInFile(outfile, "(0," + str(sizeY) + ")")
        x, y = self.convertLineToFloat(myLine, x, y)

        myLine = self.checkIfStringInFile(outfile, "(" + str(sizeX) + ",0)")
        x, y = self.convertLineToFloat(myLine, x, y)

        myLine = self.checkIfStringInFile(outfile, "(" + str(sizeX) + "," + str(sizeY) + ")")
        x, y = self.convertLineToFloat(myLine, x, y)

        return x, y

    # wydobycie konkretnej lini z gdalinfo
    def checkIfStringInFile(self, file_name, string_to_search):
        with open(self.TXT_PATH + file_name, 'r') as read_obj:
            for line in read_obj:
                if string_to_search in line:
                    return line
        return False

    # konwersja lini ze wspolrzednymi na liczby float
    def convertLineToFloat(self, line, newX, newY):
        x = line.find('>') + 3
        a = line.find(',', x, x + 50)
        wspolrzednaY = line[x: a]
        b = line.find(',', x, 100) + 1
        wspolrzednaX = line[b:line.find(',', b, b + 50)]
        newX.append(float(wspolrzednaX))
        newY.append(float(wspolrzednaY))
        return newX, newY