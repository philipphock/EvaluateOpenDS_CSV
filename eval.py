'''
Created on Mar 5, 2014

@author: phil
'''

import os


totalIterations = 0
totalTimeSpendOverSpeedLimit = 0
totalSpeedDelta = 0


lastParsedData=None
timePassedTotal=0

DATASET_PATH = "dataset"
DATASET_SUBS = ["A","B","C","D"]
DATASET_SEPARATOR=':'



def main():
    global timePassedTotal
    global lastParsedData
    global totalIterations
    global totalTimeSpendOverSpeedLimit
    global totalSpeedDelta
    
    for i in range(len(DATASET_SUBS)): 
        totalIterations = 0
        totalTimeSpendOverSpeedLimit = 0
        totalSpeedDelta = 0
        lastParsedData=None
        timePassedTotal=0
        
        print("data for %s" % DATASET_SUBS[i])
        datasetPath = getPathForDataset(i)
        for i in datasetPath:
            with open(i, 'r') as f:
                lastParsedData=None
                parsedLines=parseLines(f.readlines())
                for line in parsedLines:
                    updateStatistics(line)
    
        print(" Time passed total: %.2f s" % (timePassedTotal/1000))
        #print("Total iterations: %d" % totalIterations)
        print(" Total time spend over speed limit: %.2f s" % (totalTimeSpendOverSpeedLimit/1000))
        print(" avg kmh over speedlimit: %d" % (totalSpeedDelta/totalIterations))
        print(" -- \n")
    
    
    
'''
@return: a list of paths for the given index
@param datasetIndex: 0..4 index of DATASET_SUBS 
'''    
def getPathForDataset(datasetIndex):
    path = os.path.join(DATASET_PATH,DATASET_SUBS[datasetIndex])
    return (os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f.endswith(".txt"))
       
'''
@return: (timestamp,speed,maxAllowedSpeed) OR None on parser error
'''       
def parseLines(lines):
    for line in lines:
        splitted=line.split(DATASET_SEPARATOR)
        if len(splitted) < 3:
            continue
        if not splitted[0].isdigit():
            continue
        if float(splitted[3]) < 0:
            continue  
        yield (int(splitted[0]),float(splitted[3]),50)



def updateStatistics(parsedData):
    global lastParsedData
    global timePassedTotal
    
    global totalIterations
    global totalTimeSpendOverSpeedLimit
    global totalSpeedDelta
    
    totalIterations+=1
    
    timestamp, _, _ = parsedData
    
    if lastParsedData is None:
        lastParsedData=parsedData
        return
    else:
        lastTimestamp, lastSpeed, lastMaxAllowedSpeed = lastParsedData
        deltaT = timestamp-lastTimestamp
        timePassedTotal += deltaT
        
        deltaS = lastSpeed-lastMaxAllowedSpeed
        if (deltaS > 0):
            #over speed limit
            totalTimeSpendOverSpeedLimit+=deltaT
            totalSpeedDelta+=deltaS
        
        lastParsedData=parsedData
        


if __name__ == '__main__':
    main()


