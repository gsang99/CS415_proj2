#this is where the magic happens
from collections import deque
#parsing the input file
def parse(filename):
    file = open(filename)
    clients = []
    # for each line in file:
    for line in file:
        line = line.strip() # strip parentheses and whitespace

        if not line:  # skip empty lines
            continue

        startD, endD, rev = line.split()  # split by comma -> (s, e, rev)
        clients.append((int(startD), int(endD), int(rev)))  # append (s, e, rev) to clients

    file.close()  # close the file
    return clients

#constructing a DAG
def buildDAG(clients):
    n = len(clients)   
    START = 0 
    END = n + 1

    #making an adjency list
    adj = [[] for _ in range(n + 2)]  # adj = list of n+2 empty lists          // adj[u] holds (neighbor, weight) pairs
    hasIncoming = [False] * (n + 2)  # hasIncoming = list of n+2 falses

    # client-to-client edges, grabbing values
    for i in range(1, n + 1):  
        starti, endi, revi = clients[i - 1]  
        for j in range(1, n + 1):  
            (startj,endj,revj) = clients[j - 1]  
            if i != j and endi <= startj:  
                adj[i].append((j,revi)) 
                hasIncoming[j] = True   

    # Step 2: Start and End edges
    for i in range(1, n+1):  
        if not hasIncoming[i]:  
            adj[START].append((i,0)) 
        if not adj[i]:  
            (starti,endi,revi) = clients[i-1] 
            adj[i].append((END,revi)) 

    return adj, START, END

def sourceRemoval(adj):
    #building in degree counts
    degreeCount = [0] * len(adj)
    removalQueue = deque()
    topologicalSequence = []

    #update the in degree counts
    for i in range(len(adj)):
        for neighbor, weight in adj[i]:
            degreeCount[neighbor] += 1 
    
    #putting start in removal queue
    for i in range(len(degreeCount)):
        if degreeCount[i] == 0:
            removalQueue.append(i)
    #the source removal part
    while removalQueue:  
        vertex = removalQueue.popleft() #save vertex but remove node from removalQueue
        topologicalSequence.append(vertex)
        #iterate through adjacency list and update in degree counts after removing vertex
        for neighbor, weight in adj[vertex]:
            degreeCount[neighbor] -= 1
            #if any vertexs in degree becomes 0 add to removalQueue
            if degreeCount[neighbor] == 0:
                removalQueue.append(neighbor)
    return topologicalSequence      

def outputData(filename, numclients, maxRevenue, path):
    clientPath = ', '.join(map(str, path))
    with open(filename, 'w') as file:
        print(f"There are {numclients} clients in this file\n", file=file)
        print(f"Optimal revenue earned is {maxRevenue}", file=file)
        print(f"Clients contributing to this optimal revenue: {clientPath}", file=file)

    return



#computing the optimal path
def computeOptimalPath(adj, order, START, END):
    F = len(adj) * [0]
    opt = [None] * len(adj)

    #fill in F and opt at the same time
    for v in reversed(order):
        if v == END:
            F[END] = 0
        else:
            # w = weight on the edges leaving v
            w = adj[v][0][1]
            #best = -infinity
            best = float('-inf') 
            bestNeighbor = None
            

            for neighbor,weight in adj[v]:  
                #if F[neighbor] > best:
                if F[neighbor] > best:

                    best = F[neighbor]
                    bestNeighbor = neighbor
            F[v] = w + best
            opt[v] = bestNeighbor
    
    # // follow the opt pointers forward
    path = [] 
    v = opt[START]

    while v != END: # while v is not END:
        path.append(v)
        v = opt[v]

    # return the most amount of revenue
    return F[START], path
            

    
    
    
    

def main():
    # Your code to construct a Directed Acyclic Graph (DAG) goes here
    # clients = parse("data1.txt")
    # adj, START, END = buildDAG(clients)
    # print (adj, START, END)
    #build the DAG using the clients list and print the adjacency list, START, and END nodes

    '''
    for filename in ["data1.txt", "data2.txt"]:
        print("=== Testing", filename, "===")

        # parse the input file
        clients = parse(filename)
        print("Number of clients:", len(clients))
        print("clients:", clients)

        # build the DAG and print the adjacency list, START, and END
        adj, START, END = buildDAG(clients)
        print("START =", START, " END =", END)
        for v in range(len(adj)):
            print("adj[" + str(v) + "] =", adj[v])

        # sanity checks
        print("End has no outgoing edges:", adj[END] == [])
        print("Start edges:", [nbr for nbr, w in adj[START]])
        print()
    '''
    
    filename = input("Enter the file to read data: ")
    outFile = "out" + filename
    clients = parse(filename)
    adj, START, END = buildDAG(clients)
    topologicalSequence = sourceRemoval(adj)
    #get max revenue and client order
    maxRevenue, clientOrder = computeOptimalPath(adj,topologicalSequence, START, END)
    outputData(outFile, len(clients), maxRevenue, clientOrder)
    print(f"There are {len(clients)} clients in this file\n")
    print(f"Optimal revenue earned is {maxRevenue}")
    print(f"Clients contributing to this optimal revenue: {', '.join(map(str, clientOrder))}")
    

if __name__ == "__main__":
    main()