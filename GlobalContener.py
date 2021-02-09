class ShipContainer():
    SHIPS_PATH = "data/global_ships/"

    def __init__(self):
        self.globalShips = []

    def getGlobalShips(self):
        return self.globalShips

    def setGlobalShips(self,x,y):
        self.globalShips.append(x)
        self.globalShips.append(y)

    def createGlobalShipsTxt(self,filname):
        outfile = filname.split('.')[0] + 'MapShips.txt'
        f = open(self.SHIPS_PATH + outfile,"w")
        counter = 0
        for i in self.globalShips:
            f.write(str(i)+'\n')
            counter += 1
        f.close()
        print("save: " + outfile+"  "+ str(counter/2) + " ships found")