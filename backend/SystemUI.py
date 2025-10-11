from IPython.core.display_functions import display

from data_management import data_extraction

latitude = float(input("Enter a Latitude: "))
longitude = float(input("Enter a Longitude: "))
radius = float(input("Enter a Distance (meters): "))
# 40.4259, -86.9081
print("What would you like to do today?")
print("1. Bike")
print("2. Run")
print("3. Walk")
print("4. Exit")
option = input()
network_type = ""
if option == "1":
    network_type = "bike"
elif option == "2":
    network_type = "walk"
elif option == "3":
    network_type = "walk"
elif option == "4":
    raise SystemExit
else:
    network_type = "all"

coords = (latitude, longitude)


graph = data_extraction.get_graph(coords, radius, network_type)
nodes, edges = data_extraction.convert_graph(graph)
display(nodes.head())
display(edges.head())
