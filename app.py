import streamlit as st
import math
from MinHeap import MinHeap
from Graph import Graph, BUS, Vertex

def update_bus_info(graph, bus_type, stops):
    for stop in stops:
        vertex = graph.GetVertex(stop)
        if vertex is not None:
            vertex.SetBus(bus_type)





def DijkstrasSP(G,s,d):
	R=[]
	s.ds=0
	MH=MinHeap()
	for u in G.Vertices:
		MH.Insert(G.Vertices[u])
	MH.BuildHeap()
	while not MH.isEmpty():
		U=MH.ExtractMin()
		R.append(U.name)
		for v in U.neighbours:
			V=G.GetVertex(v)
			if V==s:
				continue
			if  V.DistFromSource()>=U.DistFromSource()+U.NeighbourWeight(v):
				V.ds=U.ds+U.NeighbourWeight(v)
				MH.UpdatePriority(V)
				V.parent=U.name


def DijkstrasST(G,s,d):
	s.ts=0
	s.ds=0
	MH=MinHeap()
	for u in G.Vertices:
		MH.Insert(G.Vertices[u])
	MH.BuildHeap()
	while not MH.isEmpty():
		U=MH.ExtractMin()
		for v in U.neighbours:
			V=G.GetVertex(v)
			if V==s:
				continue
			if U.bus['EXPRESS'] and V.bus['EXPRESS']:
				bus=BUS('EXPRESS')
			elif U.bus['SERVICE'] and V.bus['SERVICE']:
				bus=BUS('SERVICE')
			elif U.bus['CITY1'] and V.bus['CITY1']:
				bus=BUS('CITY1')
			elif U.bus['CITY2'] and V.bus['CITY2']:
				bus=BUS('CITY2')
			elif U.bus['CITY3'] and V.bus['CITY3']:
				bus=BUS('CITY3')
			elif U.bus['CITY4'] and V.bus['CITY4']:
				bus=BUS('CITY4')
			elif U.bus['CITY5'] and V.bus['CITY5']:
				bus=BUS('CITY5')
			elif U.bus['CITY6'] and V.bus['CITY6']:
				bus=BUS('CITY6')
			if bus==None:
				continue
			if (V.ts)>=(U.ts+(U.NeighbourWeight(v)/bus.speed)):
				V.ts=U.ts+(U.NeighbourWeight(v)/bus.speed)
				V.ds=U.ds+U.NeighbourWeight(v)
				MH.UpdatePriority(V)
				V.parent=U.name
				V.busFrom=bus.name
			bus=None


def DijkstrasCP(G,s,d):
	s.ts=0
	s.ds=0
	s.cs=0
	MH=MinHeap()
	for u in G.Vertices:
		MH.Insert(G.Vertices[u])
	MH.BuildHeap()
	while not MH.isEmpty():
		U=MH.ExtractMin()
		for v in U.neighbours:
			V=G.GetVertex(v)
			if V==s:
				continue
			if U.bus['CITY1'] and V.bus['CITY1']:
				bus=BUS('CITY1')
			elif U.bus['CITY2'] and V.bus['CITY2']:
				bus=BUS('CITY2')
			elif U.bus['CITY3'] and V.bus['CITY3']:
				bus=BUS('CITY3')
			elif U.bus['CITY4'] and V.bus['CITY4']:
				bus=BUS('CITY4')
			elif U.bus['CITY5'] and V.bus['CITY5']:
				bus=BUS('CITY5')
			elif U.bus['CITY6'] and V.bus['CITY6']:
				bus=BUS('CITY6')
			elif U.bus['SERVICE'] and V.bus['SERVICE']:
				bus=BUS('SERVICE')
			elif U.bus['EXPRESS'] and V.bus['EXPRESS']:
				bus=BUS('EXPRESS')
			if bus==None:
				continue
			if (V.cs>=U.cs+(U.NeighbourWeight(v)*bus.rate)):
				V.cs=U.cs+(U.NeighbourWeight(v)*bus.rate)
				V.ds=U.ds+U.NeighbourWeight(v)
				MH.UpdatePriority(V)
				V.parent=U.name
				V.busFrom=bus.name
			bus=None

def PrintPath(G, s, d):
    path = []

    def collectPath(vertex):
        nonlocal path
        if vertex.parent is not None:
            collectPath(G.GetVertex(vertex.parent))
        path.append(vertex.name)

    collectPath(G.GetVertex(d))

    if path:
        st.write("Path from", s, "to", d + ":")
        st.write(" --- ".join(path), end=' ')
        st.write("\n")
    else:
        st.write("No valid path found from", s, "to", d)




import os

def main():
    # Streamlit app title
    st.title("Local Bus Route Planner")

    image_path = r"Map.jpg"  # Replace with the path to your image file
    if os.path.exists(image_path):
        st.image(image_path, caption="MAP", use_column_width=True)
    else:
        st.warning(f"Image not found at path: {image_path}")
    # Create an empty graph
    graph = Graph()

    # Load edge weights from file
    with open(r"EdgeWeightTEMP.txt", "r") as edge_weights_file:
        for line in edge_weights_file:
            data = line.strip().split()
            if data:
                graph.AddEdge(data[0], data[1], float(data[2]))

    # Load bus information from file
    with open(r"BUSTEMP.txt", "r") as bus_file:
        for line in bus_file:
            data = line.strip().split()
            bus_type = data.pop(0)
            update_bus_info(graph, bus_type, data)

    st.write("Map formed successfully")

    # User input for source and destination
    source = st.text_input("Enter the source (From MAP):")
    destination = st.text_input("Enter the destination (From MAP):")

    # User choice for transportation mode
    transportation_mode = st.radio("Choose your mode of transport:", ["Own Transport", "Public Transport"])

    if transportation_mode == "Own Transport":
        st.write("Calculating shortest path...")
        source_vertex = graph.GetVertex(source)
        destination_vertex = graph.GetVertex(destination)

        if source_vertex and destination_vertex:
            DijkstrasSP(graph, source_vertex, destination_vertex)
            PrintPath(graph, source, destination)
            st.write("Distance:", destination_vertex.ds)
        else:
            st.write("Invalid source or destination.")

    elif transportation_mode == "Public Transport":
        st.write("Choose your priority:")
        priority = st.radio("Select Priority:", ["Shortest Time Path", "Cheapest Price Path"])

        source_vertex = graph.GetVertex(source)
        destination_vertex = graph.GetVertex(destination)

        if source_vertex and destination_vertex:
            if priority == "Shortest Time Path":
                st.write("Calculating shortest time path...")
                DijkstrasST(graph, source_vertex, destination_vertex)
                PrintPath(graph, source, destination)
                st.write("Time taken:", round(destination_vertex.ts * 60, 2), "minutes")
            elif priority == "Cheapest Price Path":
                st.write("Calculating cheapest price path...")
                DijkstrasCP(graph, source_vertex, destination_vertex)
                PrintPath(graph, source, destination)
                st.write("Price: Rs.", round(destination_vertex.cs, 2))
        else:
            st.write("Invalid source or destination.")

if __name__ == '__main__':
    main()


