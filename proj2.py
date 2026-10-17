#this is where the magic happens

#parsing the input file
def parse(filename):
    file = open(filename)
    clients = []
    # for each line in file:
    for line in file:
        line = line.strip().strip('()')  # strip parentheses and whitespace

        if not line:  # skip empty lines
            continue

        s, e, rev = line.split(',')  # split by comma -> (s, e, rev)
        clients.append((int(s), int(e), int(rev)))  # append (s, e, rev) to clients

    file.close()  # close the file
    return clients

#constructing a DAG
def DAG(clients):
    n = len(clients)  # n = length(clients)
    START = 0 # START = 0
    END = n + 1 # END = n + 1

    adj = [[] for _ in range(n + 2)]  # adj = list of n+2 empty lists          // adj[u] holds (neighbor, weight) pairs
    hasIncoming = [False] * (n + 2)  # hasIncoming = list of n+2 falses

    # client-to-client edges
    for i in range(1, n + 1):  # for i = 1 to n:
        si, ei, ri = clients[i - 1]  # (si, ei, ri) = clients[i-1]
    #     for j = 1 to n:
    #         (sj, ej, rj) = clients[j-1]
    #         if i != j and ei <= sj:
    #             add (j, ri) to adj[i]       // weight = rev of i
    #             hasIncoming[j] = true

    # // Step 2: Start and End edges
    # for i = 1 to n:
    #     if hasIncoming[i] is false:
    #         add (i, 0) to adj[START]        // weight 0
    #     if adj[i] is empty:
    #         (si, ei, ri) = clients[i-1]
    #         add (END, ri) to adj[i]         // weight = rev of i

    # return adj, START, END
    
    pass
    

def main():
    # Your code to construct a Directed Acyclic Graph (DAG) goes here
    clients = parse("input.txt")
    adj, START, end = DAG(clients)


    
    pass

if __name__ == "__main__":
    main()