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
    n = len(clients)  # n = length(clients)
    START = 0 # START = 0
    END = n + 1 # END = n + 1

    adj = [[] for _ in range(n + 2)]  # adj = list of n+2 empty lists          // adj[u] holds (neighbor, weight) pairs
    hasIncoming = [False] * (n + 2)  # hasIncoming = list of n+2 falses

    # client-to-client edges
    for i in range(1, n + 1):  # for i = 1 to n:
        starti, endi, revi = clients[i - 1]  # (si, ei, ri) = clients[i-1]
        for j in range(1, n + 1):  # for j = 1 to n:
            (startj,endj,revj) = clients[j - 1]  # (sj, ej, rj) = clients[j-1]
            if i != j and endi <= startj:  # if i != j and ei <= sj:
                adj[i].append((j,revi)) # add (j, ri) to adj[i]       // weight = rev of i
                hasIncoming[j] = True   

    # // Step 2: Start and End edges
    for i in range(1, n+1):  # for i = 1 to n:
        if not hasIncoming[i]:  #if hasIncoming[i] is false:
            adj[START].append((i,0)) # add (i, 0) to adj[START]   // weight 0
        if not adj[i]:  #if adj[i] is empty:
            (starti,endi,revi) = clients[i-1]  #  (si, ei, ri) = clients[i-1]
            adj[i].append((END,revi))  # add (END, ri) to adj[i]         // weight = rev of i

    # return adj, START, END
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
    print("\nTopological Sequence: \n")
    print(topologicalSequence)
    return topologicalSequence      

def main():
    # Your code to construct a Directed Acyclic Graph (DAG) goes here
    # clients = parse("data1.txt")
    # adj, START, END = buildDAG(clients)
    # print (adj, START, END)
    #build the DAG using the clients list and print the adjacency list, START, and END nodes


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

        topologicalSequence = sourceRemoval(adj)
    
    pass

if __name__ == "__main__":
    main()