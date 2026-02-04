from flask import Flask, request, jsonify
import geopandas as gpd
import osmnx as ox

app = Flask(__name__)



# Function that defines Specific link to return some json file
@app.route("/get-user/<userid>")
def get_user(userid):
    userData = {
        "userId": userid,
        "name": "John Downnn",
        "email": "johndown@email.com"
    }

    # Variable that gets some extra information like after ?someVar="someValue"
    extra = request.args.get("extra")
    if extra:
        userData["extra"] = extra

    return jsonify(userData), 200


@app.route("/get-shortest-path/<source>-<destination>")
def getShortestPath(source, destination):
    nodes = gpd.read_file("files/angeles_all_nodes.geojson")
    edges = gpd.read_file("files/angeles_transit_edges.geojson")
    
    nodes = nodes.set_index("osmid")
    nodes.index = nodes.index.astype(int)
    nodes.index.name = "osmid"

    # 2. Ensure edges reference the same IDs
    edges["u"] = edges["u"].astype(int)
    edges["v"] = edges["v"].astype(int)
    edges["key"] = edges["key"].astype(int)

    edges = edges.set_index(["u", "v", "key"])

    # 3. CRS must match
    nodes = nodes.to_crs(edges.crs)

    G = ox.graph_from_gdfs(nodes, edges)


    computedShortestPath = ox.routing.shortest_path(G, source, destination, weight="weight")
    gdfShortestPath = ox.routing.route_to_gdf(G, computedShortestPath)

    return gdfShortestPath

if __name__ == "__main__":
    app.run(debug=True)

