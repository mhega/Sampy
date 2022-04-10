#**************************************************
# AnalyzeTop V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 4/10/2022
#**************************************************

from Table import Table
import re
import sys

class Top:
    def __init__(self,file, nodeName):
        self.fileName = file
        self.nodeName = nodeName

    def loadtop(self, *, fhand):
        currentNode = None
        currentTable = Table([])
        headerNames = []
        prevTopRunTime = ''
        topRunTime = ''
        topCtx = {}
        nodeName = self.nodeName

        for line in fhand:
            if len(line.strip().split()) > 6:
                if re.search('.*PID.*',line): # Looking for known excerpt to distinguish header from data
                    if len(headerNames) == 0:
                        headerNames = line.strip().split()
                        currentTable.setHeaderNames(headerNames)
                    if len(currentTable.data) > 0:
                        topCtx.setdefault(nodeName, []).append((currentTable,prevTopRunTime))
                        currentTable = Table(headerNames)
                elif len(line.strip().split()) == len(headerNames) and line.strip().split()[0].isnumeric(): # Data
                    currentTable.append(tuple(line.strip().split()))
                elif re.search('^top - (\d\d:\d\d:\d\d)', line):
                    prevTopRunTime = str(topRunTime)
                    topRunTime = re.findall('^top - (\d\d:\d\d:\d\d)', line)[0]
            #elif len(line.strip().split()) > 1: # incomplete or unrecognicable data. Generating debug log is out of scope of this exercise
            #    utils.debug(('Unknown line: '+line).strip())
            #    utils.debug('Current node at line: %s\n ' % currentNode)
        topCtx.setdefault(nodeName, []).append((currentTable,topRunTime))

        return topCtx

    @Table.filtertabledata
    def merge(self, *_tables):
        def aggr(x):
            _theList = [int(float(x[_sumHeader.index('%CPU')])) for x in filter(lambda y:y[_sumHeader.index('PID')] == x[_sumHeader.index('PID')], _sumData)]
            return (sum(_theList), len(_theList), int(sum(_theList) / len(_theList)))
        _sum = sum(_tables,Table(_tables[0].headerNames))
        #print('Sum: ',len(_sum.data))
        _sumHeader = _sum.headerNames
        _sumData = sorted(_sum.data, key=lambda x:int(float(x[_sumHeader.index('%CPU')])), reverse=True)
        _uniqueData = [_sumData[i] for i in filter(lambda x:_sumData[x][_sumHeader.index('PID')] not in [y[_sumHeader.index('PID')] for y in _sumData[:x]], range(len(_sumData)))]
        cpupctthreshold = -1    # Customizable to allow filtering only tasks with CPU% that are higher than this value.
        targetHeader = _sumHeader+['NumTimes','Avg%CPU']
        _resortedUniqueData = list(filter(lambda x : int(x[targetHeader.index('Avg%CPU')]) > cpupctthreshold, [t+aggr(t)[1:] for t in sorted(_uniqueData, key = aggr, reverse=True)]))
        return Table(targetHeader, _resortedUniqueData)

    def analyze(self):
        import ListTables
        fhand = None
        
        if self.fileName is not None:
            fhand=open(self.fileName)
            if fhand is None:
                exit()
        else:
            exit() # We should never be here since our constructor should have initialized filename.

        self.loadData(fhand = fhand)

        _consolidatedTopCtx = {}

        for nodeName in self.topCtx.keys():
            _consolidatedTopCtx[nodeName] = self.merge(*[a for a,b in self.topCtx[nodeName]]
            , filterFunc = lambda x:float(x('%CPU')) > 0
            ).get(('PID','COMMAND','NumTimes','Avg%CPU'))

            #_consolidatedTopCtx[nodeName] = [(a,b,(lambda x:x if x and int(c) == 4 else '')(self.getSession(nodeName,b,a)),c,d) for a,b,c,d in _consolidatedTopCtx[nodeName]]

        tasksPerNode = 20      
        print('\n\n'+ListTables.underline('Top analysis summary by highest sum(%%CPU):' ))

        print('\nTasks are sorted in descending order according to each task\'s sum of all reported CPU pecentage value snapshots'+
        '\nThis is to ensure both the CPU% value and task persistence are taken into accout during sorting of task significance.')

        ListTables.printTablesSideways(
            ('PID','CMD','TimesSeen','Avg%CPU')         # tableHeader
            , _consolidatedTopCtx                       # tableCtx
            , tasksPerNode, 2, 1          # allowedTabLength, tablesPerLine, topListToPrint
            , key=lambda x: 0 if len(x) == 0 else (int(x[0][2])*int(x[0][3]))
            , reverse=True
            , frameBlock='.'
            )


    def loadData(self,*, fhand = None):
        if fhand is not None:    
            self.topCtx = self.loadtop(fhand = fhand)

args = sys.argv

if len(args[1]) > 4:
    filename = args[1]
    run = Top(filename, 'Top')
    run.analyze()

