from matplotlib import pyplot
import sys
import random
import time

class TSP:

    def __init__(self, filename):
        self.filename = filename
        ### self.filename is the csv data file which read by the program
        self.cities = self.readFile()
        ### self.cities is a list of lists of the form:
        self.matrix = self.buildMatrix()
        ### self.matrix is a matrix (list of lists) of distances
        ### between pairs of cities.
        ### Indexes are one to one mapped with self.cities indexes.
        self.tour = []
        ### Current solution: an ordering of all city indexes

##  read the csv data file and put the data into the self.cities
    def readFile(self):
        cityList = []
        f = open(self.filename,'r')
        for line in f:
            tempList = line.split(';')
            tempList[2] = tempList[2].rstrip('\n')
            cityList.append(tempList)
        f.close()
        return cityList
    
## build the matrix of distances between pairs of cities
    def buildMatrix(self):
        matrixLen = len(self.cities);
        matrix = [[0 for i in range(matrixLen)]for j in range(matrixLen)]
        for i in range(matrixLen):
            for j in range(matrixLen):
                matrix[i][j] = self.distance(i, j)
   
        return matrix
    
### Distance between the two cities at indexes i and j
    def distance(self,i,j):
        x1 = int(self.cities[i][1])
        y1 = int(self.cities[i][2])
        x2 = int(self.cities[j][1])
        y2 = int(self.cities[j][2])
        dis = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        return round(dis)
    
## the total distance of the cycle tour
    def totalDistance(self, cityIndexes):
        ### Total ditance corresponding to the ordering in self.tour
        sumDistance = 0
        l  = len(cityIndexes)
        for i in range(l - 1):
            sumDistance += self.distance(cityIndexes[i], cityIndexes[i + 1])
        return sumDistance
    
## print the city names corresponding to the ordering  in self.tour
## print the best found distance by the algorithm
    def printIt(self, dis):
        l = len(self.tour)
        index = 0
        print('Best Found Distance:',dis,'miles')
        for cityIndex in self.tour:
           if(index == l - 1):
               print(self.cities[cityIndex][0])
           else:
               print(self.cities[cityIndex][0],'- ', end = '')
           index += 1
        print('\n\n')



## dispaly the Pyplot of the solution tour       
    def plotIt(self):
        ## A random tour would be dispalyed in black line
        x = []
        y = []
        for city in self.cities:
            x.append(city[1])
            y.append(city[2])
        pyplot.plot(x, y, 'Black')   
        ## The solution (best found) tour would displayed in blue line
        tourX = []
        tourY = []
        for res in self.tour:
            tourX.append(self.cities[res][1])
            tourY.append(self.cities[res][2])
##          uncommon the following code to add the city name
##            pyplot.text(self.cities[res][1], self.cities[res][2], self.cities[res][0])
        pyplot.plot(tourX, tourY, color = 'Blue', linewidth = 2.5)
        pyplot.show()


## The method of finding the optimal solution of the min distance
## This method will call the greedy algorithm to get a solution first
## Than if would call local search algorithm to improve the solution
    def solve(self):
        minDistance = sys.maxsize
        bestTour = []
## Find the minimize distance tour of all route started with each city
## Each distance are calculated by greedy algorithm
        for startCity in range (len(self.cities)):
            newTour = self.greedy(startCity)
            newDistance = self.totalDistance(newTour)
            if(newDistance < minDistance):
                minDistance = newDistance
                bestTour = newTour
## Improve the solution by the local search algorithm
        bestTour = self.localSearch(bestTour, minDistance)
        return bestTour
    

        
## Greedy algorithm which would find the minimize distance of the
## current city each time
    def greedy(self, startCity):
        ## indexes would record the index of city which has not been
        ## visited by the tour
        visitedRecord = [i for i in range(len(self.cities))]
        count = 0
        result = [startCity]
        currentCity = startCity
        visitedRecord[currentCity] = -1
        while(count != len(self.cities) - 1):
            nextCity = self.minDistance(currentCity, visitedRecord)
            result.append(nextCity)
            visitedRecord[nextCity] = -1
            currentCity = nextCity
            count += 1
        result.append(startCity)
        return result

## Return the city which have minimize distance from the city in cityIndex
## the method would check the visitedRecord if city has been visited
    def minDistance(self, city, visitedRecord):
        minDis = sys.maxsize
        minIndex = -1
        for i in visitedRecord:
            if i != -1 and i != city:
                dis = self.distance(city, i)
                minDis = min(dis, minDis)
                if(minDis == dis):
                    minIndex = i
        return minIndex

## Return a new tour which swaped the tour[x] and tour[y]
##  Also the tour[x + 1] to tour[y - 1] should be reversed
##  In this way we can swap two edges in the whole graph
    def swap(self, tour, x, y):
        newTour = list(tour)
        l = len(newTour)
        j = y
        for i in range(x, y+1):
            newTour[i] = tour[j]
            j -= 1
        if(newTour[l - 1] != newTour[0]):
            newTour[l - 1] = newTour[0]
        return newTour

 
## It is a complete 2-opt local search, it could improve the result by reorder
## the route which has crosses over itself.
    def localSearch(self, tour, distance):
        l = len(tour)
        minDis = distance
        minTour = tour
        improve = True
##  Swap each pair of city in the route 
        while(improve):
            for i in range(l - 2):
                for j in range(i + 1, l - 1):
                    newTour = self.swap(minTour, i, j)
                    newDis = self.totalDistance(newTour)
                    if(newDis < minDis):
                        minTour = newTour
                        minDis = newDis
                        improve = True
            improve = False
        return minTour
    
### A test to computes a tour for one of the data files
### and then prints out and displays on Pyplot the solution                   
    def test(self):
        t0 = time.time()
        self.tour = self.solve()
        dis = self.totalDistance(self.tour)
        t1 = time.time()
        print('total time is', str(t1 - t0))
        self.printIt(dis)
        self.plotIt()

## The interact way to test the TSP solution
def interact():
    while(True):
        filename = input('Please input the data file name you want to solve TSP problem.\n ')
        tsp = None
        try:
            tsp = TSP(filename)
        except:
            print('The file cannot be open !', filename,'might not exist.')
        if(tsp):
            tsp.test()
interact()




        
