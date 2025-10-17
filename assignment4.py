from asyncio.windows_events import NULL
from cmath import inf

def allocate(preferences, sysadmins_per_night, max_unwanted_shifts, min_shifts):
    """
    Function allocates shifts for admins, given the exact number of admins
    needed per night, maximum shifts that an admin can take and the minimum
    shifts that an admin needs to take.

    Input:
        preferences: a matrix that represents the preference of each admin
        sysadmins_per_night: exact number of admins needed per night
        max_unwanted_shifts: maximum number of shifts that an admin can take that is not their preference
        min_shifts: minimum number of shifts any one admin needs to take
    Output:
        a matrix that shows the schedule of the admins
    Time complexity:
        Best: O(N^2)
        Worst: O(N^2)
        where N = number of system admins
    
    Space complexity:
        Input: O(N) where N = number of timelines in timelines
        Aux: O(1)
    """
    numOfDays = len(preferences)
    numOfAdmins = len(preferences[0])
    numOfVertex = numOfDays + (numOfAdmins*2) + numOfAdmins + 4
    graph = MyGraph(numOfVertex)
    edgesFromSource = [None] * numOfAdmins
    totalPreferencedDays = [0] * numOfAdmins

    #find total number of prefered days by each admin
    for j in range(numOfAdmins):
        for i in range(numOfDays):
            totalPreferencedDays[j] += preferences[i][j] 

    #add edge for admin vertices
    for j in range(numOfAdmins):
        edgesFromSource[j] = Edge(0,j+1,totalPreferencedDays[j]+max_unwanted_shifts-min_shifts)
    graph.add_edges(edgesFromSource)
    
    edgesFromAdmins = [None]*(numOfAdmins*2)
    #vertex that takes unwanted shifts has an index of n+(k*2)-1 where k=index of admin vertex
    #vertex that takes prefered shifts has an index of n+(k*2) where k= index of admin vertex
    iterIndex = 0
    for i in range(numOfAdmins):
        edgesFromAdmins[iterIndex] = Edge(i+1,numOfAdmins+((i+1)*2)-1,max_unwanted_shifts)
        edgesFromAdmins[iterIndex+1] = Edge(i+1, numOfAdmins+((i+1)*2),totalPreferencedDays[i])
        iterIndex +=2
    graph.add_edges(edgesFromAdmins)

    #add edges to night shift vertices
    for day in range(1,numOfDays+1):
        for admin in range(1,numOfAdmins+1):
            if preferences[day-1][admin-1] == 1:
                graph.add_edges([Edge((admin*2)+numOfAdmins,(numOfAdmins*3)+day,1)])
            elif preferences[day-1][admin-1] == 0:
                graph.add_edges([Edge((admin*2)-1+numOfAdmins,(numOfAdmins*3)+day,1)])
        graph.add_edges([Edge((3*numOfAdmins) + day,len(graph.vertices)-3, sysadmins_per_night)])

    graph.add_edges([Edge(numOfVertex-2,0,(sysadmins_per_night*numOfDays))])
    graph.add_edges([Edge(numOfVertex-3,numOfVertex-1,(sysadmins_per_night*numOfDays))])

    network = NetworkFlow(graph)
    network.fordFulkerson()
    if graph.vertices[numOfVertex-2].edges[0].potential() != 0:
        return None
    return scheduleTable(graph,preferences)

def scheduleTable(graph,preferences):
    """
    Function populates a matrix to show the schedule for the admins shift

    Precondition: ford fulkerson applied on graph to find maximum flow
    Postcondition:
    
    Input:
    graph: a graph that is turned into a network flow
    preferences: the matrix that represents system admin's shift preferences
    Output:
        None
    Time complexity:
        Best: O(N^2)
        Worst: O(N^2)
        where N = number of system admins
    
    Space complexity:
        Input: O(N) where N = number of system admins
        Aux: O(1)
    """
    #vertex that takes unwanted shifts has an index of n+(k*2)-1 where k=index of admin vertex
    #vertex that takes prefered shifts has an index of n+(k*2) where k= index of admin vertex
    for i in range(len(preferences[0])):
        for edge in graph.vertices[i+1].edges: #edge from a 
            if edge.isResidual() == False:
                for edgeToDay in graph.vertices[edge.v].edges: #edgeToDay are edges from u/w 
                    if edgeToDay.isResidual() == False:
                        index = abs(edgeToDay.v -30-1)
                        preferences[index][i] = edgeToDay.flow
    return preferences

class MyGraph:

    """
    Class represents weighted directed graph strucutre
    """

    def __init__(self,n):
        """
        Initialize this class object that represents a directed graph data structure
        that has vertices and edges.

        Input:
            n: number of vertices
        Output:
            None
        Time complexity:
            Best: O(N)
            Worst: O(N)
            where N = number of vertices
    
        Space complexity:
            Input: O(1)
            Aux: O(N) where N = number of vertices
        """
        self.vertices = [None] * n
        for i in range(n):
            self.vertices[i] = Vertex(i)

    def add_edges(self, edges):
        """
        Function appends edges to the list of edges in the vertex

        Input:
            edges: a list of edges to be added into their respective vertices
        Output:
            None
        Time complexity:
            Best: O(M)
            Worst: O(M)
            where M = number of edges
    
        Space complexity:
            Input: O(M) where M = number of edges
            Aux: O(1)
        """
        for edge in edges:
            residualEdge = Edge(edge.v,edge.u,0)
            edge.residual = residualEdge
            residualEdge.residual = edge
            self.vertices[edge.v].add_edge(residualEdge)
            self.vertices[edge.u].add_edge(edge)

class Vertex:

    """
    Class represents a vertex (or a node) of a graph
    """

    def __init__(self,name):
        """
        Function initializes a vertex object

        Input:
            name: name of vertex
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.name = name
        self.edges = []
        self.visited = False

    def add_edge(self,edge):
        """
        Function appends an edge object to the edges list of this object

        Input:
            edge: edge to be appended
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.edges.append(edge)

class Edge:

    """
    Class represents an edge in a graph that is directed and weighted.
    It also has a flow and residual attribute, where flow is the flow
    in the edge and residual is the residual edge of it.
    """
    
    def __init__(self,u,v,capacity):
        """
        Function initializes an edge object

        Input:
            u: the name of the originating vertex of this edge
            v: the name of the receiving vertex of this edge
            capacity: the maximum weight of this edge
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)

        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.residual = NULL
    
    def isResidual(self):
        """
        Function returns true if this edge is a residual edge, false otherwise.

        Input:
            None
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        return self.capacity == 0

    def augment(self,bottleNeck):
        """
        Function augments the edge by subtracting flow from its residual edge
        and adding flow to itself.

        Input:
            bottleNeck: the minimum residual flow from an augmented path
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.flow += bottleNeck
        self.residual.flow -= bottleNeck

    def potential(self):
        """
        Function returns the remaining capacity of the edge which
        is also known as its potential.

        Input:
            None
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        return self.capacity - self.flow


class NetworkFlow:
    def __init__(self, graph) :
        """
        Function initializes a networkflow object

        Input:
            graph: a graph that represents the network flow
            preferences: the matrix that represents system admin's shift preferences
        Output:
            None
        Time complexity:
            Best: O(N^2)
            Worst: O(N^2)
            where N = number of system admins
    
        Space complexity:
            Input: O(V+E) where V = number of vertices, E = number of edges
            Aux: O(1)
        """
        self.graph = graph
        self.numOfVertex = len(graph.vertices)
        self.source = graph.vertices[len(graph.vertices)-2]
        self.target = graph.vertices[-1]

    def fordFulkerson(self):
        """
        Function finds the maximum flow of a networkflow structure.
        Referenced from https://www.youtube.com/watch?v=Xu8jjJnwvxE

        Input:
            None
        Output:
            None
        Time complexity:
            Best: O(V)
            Worst: O(V)
            where V = number of vertices
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        while self.hasAugmentPath(self.source,inf) != 0:
            self.makeAllVertexUnvisited()

    def hasAugmentPath(self,vertex,pathFlow):
        """
        Function performs dfs to check whether there is an augmenting path
        and augments the path if there is one.

        Input:
            vertex: the starting source to find augmenting path
            pathFlow: the minimum potential in the path
        Output:
            minimum potential in the path to be augmented

        Time complexity:
            Best: O(V)
            Worst: O(V)
            where V = number of vertices in the graph
    
        Space complexity:
            Input: O(1) 
            Aux: O(1)
        """
        if vertex.name == self.target.name:
            return pathFlow
        
        self.visited(vertex.name)
        for edge in vertex.edges:
            if edge.potential() > 0 and self.graph.vertices[edge.v].visited == False:
                bottleNeck = self.hasAugmentPath(self.graph.vertices[edge.v], min(pathFlow,edge.potential()))
                if (bottleNeck > 0):
                    edge.augment(bottleNeck)
                    return bottleNeck
        return 0

    def visited(self,i):
        """
        Function sets visited attribute to true for vertex i

        Input:
            i: the name of vertex to be checked
        Output:
            None
        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.graph.vertices[i].visited = True

    def makeAllVertexUnvisited(self):
        """
        Function sets the visited attribute of all vertices in graph to false

        Input:
            None
        Output:
            None
        Time complexity:
            Best: O(V)
            WorstL O(V)
            where V = number of vertex
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        for vertex in self.graph.vertices:
            vertex.visited = False

#___________________________________________________________________________________________________________________________________#
# Q2
#___________________________________________________________________________________________________________________________________#

class EventsTrie:

    """
    Class that represents a generalized suffix trie data structure where it
    encapsulates the all of the timelines (words) and their corresponding events (characters).
    """

    def __init__(self, timelines):
        """
        Function initializes the eventstrie object

        Input:
            timelines: a list of timelines
        Output:
            None
        Time complexity:
            Best: O(NM^2)
            Worst: O(NM^2)
            where
            N = number of timelines in timelines
            M = number of events in the longest timeline
    
        Space complexity:
            Input: O(N) where N = number of timelines in timelines
            Aux: O(M) where M = number of events in the longest timeline
        """
        self.root = Event()
        self.level_events = [None] * (self.max_timeline_len(timelines)+1) #events that exist in each level

        #initialize level_events
        for i in range(len(self.level_events)):
            self.level_events[i] = []

        #insert event suffixes
        for i in range(len(timelines)):
            timeline = timelines[i]
            for j in range(len(timeline)):
                subevents = timeline[j:]
                self.insert(subevents,i)

    def insert(self,subevents,i):
        """
        Function inserts the subset of events into the suffix trie.

        Input:
            subevents: a subset of events in the timeline
            i: ith timeline
        Output:
            None

        Time complexity:
            Best: O(M)
            Worst: O(M)
            where M = number of events in the longest timeline
    
        Space complexity:
            Input: O(M) where M = number of events in the longest timeline
            Aux: O(1)
        """
        current = self.root
        lvl = 1
        for event in subevents:
            index = ord(event)-97+1
            if current.next[index] is None:
                current.next[index] = Event(timeline_i=i,level = lvl,chain = current.chain+event)
                self.level_events[lvl].append(current.next[index])
                current = current.next[index]
            else:
                current.next[index].check_timeline(timeline_i = i)
                current = current.next[index]
            lvl+=1

    def getLongestChain(self,noccurence):
        """
        Function finds the longest chain of events that has occured at least K times where K
        is the number given as an input.

        Input:
            noccurence = the least number of times the chain of events has happened
        Output:
            a longest string of events that has occured at least K times here K
            is the number given as an input.

        Time complexity:
            Best: O(1)
            Worst: O(K)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        for lvl in range(len(self.level_events)-1,-1,-1):
            for event in self.level_events[lvl]:
                if event.count >= noccurence:
                    return event.chain
    
    def max_timeline_len(self,timelines):
        """
        Calculates and returns the number of events in the longest timeline.

        Input:
            timelines = list of timelines where each timeline containts a list of events
        Output:
            the number of events in the longest timeline.

        Time complexity:
            Best: O(N)
            Worst: O(N)
            where N = number of timelines in timelines
    
        Space complexity:
            Input: O(N) where N = number of timelines in timelines
            Aux: O(1)
        """
        max_len = 0
        for timeline in timelines:
            max_len = max(len(timeline),max_len)
        return max_len

class Event:
    def __init__(self,size = 27,timeline_i = -1,level = 0,chain = ""):
        """
        Initialize Event object. Has an attribute "count" that stores the
        number of times that this event has occured from each timeline.
        Attribute "next" is the next event that follows after the current event.

        Input:
            size: the number of unique events
            timeline_i: the ith timeline
            level: the level of this event starting from the root
            chain: the chain of events up till this event

        Output:
            None

        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.next = [None] * size
        self.count = 1
        self.current_timeline = timeline_i
        self.level = level
        self.chain = chain
    
    def check_timeline(self,timeline_i):
        """
        Checks whether the event that is currently being entered
        belongs to the same or different timeline. Increment count if different
        and do nothing otherwise.

        Input:
            timeline_i = the ith timeline in timelines
        Output:
            None

        Time complexity:
            Best: O(1)
            Worst: O(1)
    
        Space complexity:
            Input: O(1)
            Aux: O(1)
         """
        if (timeline_i != self.current_timeline):
            self.current_timeline = timeline_i
            self.count +=1