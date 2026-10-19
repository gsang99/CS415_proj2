#this is where the magic happens

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

#computing the optimal path
def computeOptimalPath(adj, START, END):
    #optimal path from start to end vertex can be computer very fast as follows

    #bullet 1: recurrence we already know
        #F(vi) = wi + max F(of each neighbor)
        # the best you can earn from vertex vi to end is the weight of
        #the edge leaving vi, plus the best result among all the vertices
        #you could go to next
    
    #peusdo code:
    #for the sort list i start from the end and iterate backwards from end to start
        #at each vertex fill in F and opt
        #
    #bullet 2: the opt pointer
        #while computing the max, you also remember which neighbor won
        #thats what arg means: max operation gives you a value and arg 
        #gives you the identity of whatever produced it
        #opt[vi] = next vertex to move from to vi if i want the best outcome
        #you fill in opt at the same time as F, in the same loop
        #fill in opt at the same time as f in the same loop for each vertex
    #Bullet 3: following the pointers.
        # Once F and opt are filled in for every vertex, the best path is just a chain:

        # Start at opt[Start]. That’s the first client in the optimal set.
        # Look up opt of that client. That’s the next client.
        # Keep going until you reach End, then stop.

        # Each vertex you visit along the way (excluding Start and End, which aren’t real clients) is one client in the optimal set.

        # Why it works: F[Start] was built from the best choice at every step, so following 
        # those same best choices from the top retraces the winning path. 
        # No searching or recomputing is needed, just lookups, which is why the spec calls it “very fast.”
    pass
    
    

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

    
    pass

if __name__ == "__main__":
    main()