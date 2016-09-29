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
        print('read !! file !')
        for line in f:
            tempList = line.split(';')
            tempList[2] = tempList[2].rstrip('\n')
            cityList.append(tempList)
        f.close()
        print(cityList)
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
       # print('cityIndex0', cityIndexes[0])
##      sumDistance += self.distance(cityIndexes[0], cityIndexes[l - 2])
        return sumDistance
    
## print the city names corresponding to the ordering  in self.tour
## print the best found distance by the algorithm
    def printIt(self, dis):
        ### Prints out the solution on IDLE, exactly as stated in the slides
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
##        print('Improved Distance:', self.improvedDis)
##        for cityIndex in self.improvedTour:
##           print(self.cities[cityIndex][0],'- ',end ='')


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
            pyplot.text(self.cities[res][1], self.cities[res][2], self.cities[res][0])
        pyplot.plot(tourX, tourY, color = 'Blue', linewidth = 2.5)
        pyplot.show()

##        improvedresX = []
##        improvedresY = []
##        for res in self.improvedTour:
##            improvedresX.append(self.cities[res][1])
##            improvedresY.append(self.cities[res][2])
##            pyplot.text(self.cities[res][1],self.cities[res][2], self.cities[res][0])
##        pyplot.plot(improvedresX, improvedresY, color = 'Red', linewidth = 2.5)
##        pyplot.show()

## The method of finding the optimal solution of the min distance
## This method will call the greedy algorithm to get a solution first
## Than if would call local search algorithm to improve the solution
    def solve(self):
        minDistance = sys.maxsize
        bestTour = []
 
        for startCity in range (len(self.cities)):
            newTour = self.greedy(startCity)
##            newOrder = self.improve(newOrder,1000)
##            newOrder = self.superImprove(newOrder)
            newDistance = self.totalDistance(newTour)
            if(newDistance < minDistance):
                minDistance = newDistance
                bestTour = newTour
        bestTour = self.localSearch(bestTour, minDistance)
        return bestTour
    
##    def randomSolve(self):
##        l = len(self.cities)
##        random.seed(525)
##        cityIndex = random.randrange(0,l - 1)
##        res = self.greedy(cityIndex)
##        res = self.improve(res, 2000)
##        return res
        
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
## the method would check the indexes if city has been visited
    def minDistance(self, cityIndex, indexes):
        minDis = sys.maxsize
        minIndex = -1
        for i in indexes:
            if i != -1 and i != cityIndex:
                dis = self.distance(cityIndex, i)
                minDis = min(dis, minDis)
                if(minDis == dis):
                    minIndex = i
        return minIndex

##    def randomMove(self, tour, seedNum):
##        random.seed(seedNum)
##        index1 = random.randrange(0, len(tour) - 2)
##        index2 = random.randrange(0, len(tour) - 2)
##        #print('random index', index1, index2)
##        newTour = self.swap(tour, index1, index2)
##        return newTour

##
##    def improve(self, tour, limit):
##        minTour = tour
##        minDis = self.totalDistance(minTour)
##        count = limit
##        while count > 0:
##            seed = count
##            newTour = self.randomMove(minTour, seed)
##            newDis = self.totalDistance(newTour)
##            #print('newTour is', newTour)
##            #print('newTour distance is', self.totalDistance(newTour))
##            if(newDis  < minDis):
##              # print('improved!!')
##                count = limit
##                minDis = newDis
##                minTour = newTour
##            count -= 1
##           
##        count = limit
##            
##        return minTour

##    def swap(self, tour, x, y):
##        newTour = list(tour)
##        l = len(newTour)
##        temp = newTour[x]
##        newTour[x] = newTour[y]
##        newTour[y] = temp
##        if(newTour[l - 1] != newTour[0]):
##            newTour[l - 1] = newTour[0]
##        return newTour
    
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

 
    
    def localSearch(self, tour, distance):
        l = len(tour)
        minDis = distance
        minTour = tour
        improve = True

        while(improve):
            for i in range(l - 2):
                for j in range(i + 1, l - 1):
                    newTour = self.swap(minTour, i, j)
                    newDis = self.totalDistance(newTour)
                    if(newDis < minDis):
                        minTour = newTour
                        minDis = newDis
##                        print("new improved", minDis, 'exchange', i, j)
                        improve = True
            improve = False
        return minTour
                    
  
    ### Main algorithms:
    ### 1- Greedy
      # You will need at least two methods:
      # - Select the closest city index to a given city
      # - Main procedure
    ### 2- Local search (if any)
      # You will need at least two methods:
      # - Make a move
      # - Main procedure
    
    def test(self):
        ### Write a call that computes a tour for one of the data files
        ### and then prints out and displays on Pyplot the solution
        ### Replace the above statement by your code
##        self.tour = self.randomSolve()
        t0 = time.time()
        self.tour = self.solve()
        dis = self.totalDistance(self.tour)
        t1 = time.time()
        print('total time is', str(t1 - t0))
        self.printIt(dis)
        self.plotIt()
##        self.improvedTour = self.superImprove(self.tour)
##        self.improvedDis = self.totalDistance(self.improvedTour)

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




        
