from flask import Flask, request, jsonify
import geopandas as gpd
import osmnx as ox

app = Flask(__name__)

# Test
@app.route("/test/<num>")
def get_user(num):
    userData = {
        "Hello World!": num
    }
    return jsonify(userData), 200

# Function that defines Specific link to return some json file
@app.route("/get-user/<userid>")
def get_user(userid):
    userData = {
        "userId": userid,
        "name": "John Down 2",
        "email": "johndown@email.com"
    }

    # Variable that gets some extra information like after ?someVar="someValue"
    extra = request.args.get("extra")
    if extra:
        userData["extra"] = extra

    return jsonify(userData), 200


@app.route("/get-shortest-path")
def getShortestPath():

    source = int(request.args.get("source"))
    destination = int(request.args.get("destination"))


    print("Testing")
    nodes = gpd.read_file("files/angeles_all_nodes.geojson")
    edges = gpd.read_file("files/angeles_transit_edges.geojson")
    print("Tested")

    nodes = nodes.set_index("osmid")
    nodes.index = nodes.index.astype(int)
    nodes.index.name = "osmid"

    print(1)
    # 2. Ensure edges reference the same IDs
    edges["u"] = edges["u"].astype(int)
    edges["v"] = edges["v"].astype(int)
    edges["key"] = edges["key"].astype(int)
    print(2)
    edges = edges.set_index(["u", "v", "key"])
    print(3)
    # 3. CRS must match
    nodes = nodes.to_crs(edges.crs)
    print(4)
    G = ox.graph_from_gdfs(nodes, edges)

    # print(nodes.head())
    # print(edges.head())
    print(5)




    computedShortestPath = ox.routing.shortest_path(G, source, destination, weight="weight")
    print(6)
    gdfShortestPath = ox.routing.route_to_gdf(G, computedShortestPath)
    print(7)

    import numpy as np
    for col in gdfShortestPath.columns:
        gdfShortestPath[col] = gdfShortestPath[col].apply(
            lambda x: x.tolist() if isinstance(x, np.ndarray) else x
        )
        
    return jsonify(gdfShortestPath.to_json()), 200

if __name__ == "__main__":
    app.run(debug=True)

