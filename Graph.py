import math
from MinHeap import MinHeap
c2=0
class Vertex:
	def __init__(self,name):
		self.name=name
		self.neighbours={}
		self.ds=math.inf
		self.parent=None
		self.busFrom= None
		self.MHListIndex=None
		self.bus={'EXPRESS':False,'SERVICE':False,'CITY1':False, 'CITY2':False, 'CITY3': False, 'CITY4': False, 'CITY5': False, 'CITY6': False}
		self.ts=math.inf
		self.cs=math.inf

	def Addneighbour(self, name, weight=0):
		self.neighbours[name]=weight

	def __str__(self):
		return str(self.name) + ' neighbours are ' + str([x for x in self.neighbours.keys()])

	def NeighbourWeight(self, nbr):
		if nbr in self.neighbours:
			return self.neighbours[nbr]

	def DistFromSource(self):
		return self.ds

	def SetBus(self,bustype):
		self.bus[bustype]=True

	def TimeFromSource(self):
		return self.ts

	def __lt__(self,other):
		global c2
		if c2==0:
			if self.ds<other.ds:
				return True
			elif self.ds>other.ds:
				return False
		elif c2==1:
			if self.ts<other.ts:
				return True
			elif self.ts>other.ts:
				return False
		elif c2==2:
			if self.cs<other.cs:
				return True
			elif self.cs>other.cs:
				return False


class BUS:

	def __init__(self,name):
		self.name=name
		if name=='EXPRESS':
			self.speed=75
			self.rate=1.5
		elif name=='CITY1' or name=='CITY2' or name=='CITY3' or name=='CITY4' or name=='CITY5' or name=='CITY6' :
			self.speed=30
			self.rate=0.56
		elif name=='SERVICE':
			self.speed=40
			self.rate=1


class Graph:

	def __init__(self):
		self.nv=0
		self.Vertices={}

	def __iter__(self):
		return iter(self.Vertices.values())

	def AddVertex(self,name):
		self.nv=self.nv+1
		NewVertex=Vertex(name)
		self.Vertices[name]=NewVertex
		return NewVertex

	def AddEdge(self,Head,Tail,weight):
		if Head not in self.Vertices:
			self.AddVertex(Head)
		if Tail not in self.Vertices:
			self.AddVertex(Tail)
		self.Vertices[Head].Addneighbour(Tail,weight)
		self.Vertices[Tail].Addneighbour(Head,weight)

	def GetVertex(self,name):
		if name in self.Vertices:
			return self.Vertices[name]

	def UpdateBusInfo(self,bustype,l):
		for i in range(0,len(l)):
			self.GetVertex(l[i]).SetBus(bustype)

	def GetVertices(self):
		return self.Vertices.keys()
