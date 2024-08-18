import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import numpy as np


def generate_hex_grid(bounds, hex_size):
    """Generate a hexagonal grid within the bounds."""
    xmin, ymin, xmax, ymax = bounds
    width = hex_size * 2
    height = np.sqrt(3) * hex_size
    cols = int(np.ceil((xmax - xmin) / width)) * 2 + 1
    rows = int(np.ceil((ymax - ymin) / height)) + 1
    hexagons = []
    for row in range(rows):
        for col in range(cols):
            x = xmin + col * width * 0.75
            y = ymin + row * height + (col % 2) * height / 2
            hexagon = Polygon([
                (x + hex_size * np.cos(np.pi / 3 * i), y + hex_size * np.sin(np.pi / 3 * i))
                for i in range(6)
            ])
            hexagons.append(hexagon)
    return hexagons


def hex_grid_to_geodataframe(hexagons, crs):
    """Convert a list of hexagons to a GeoDataFrame."""
    return gpd.GeoDataFrame({'geometry': hexagons}, crs=crs)


# Load the shapefile
shapefile_path = './test/Export_Output1111.shp'
gdf = gpd.read_file(shapefile_path)

# Define the size of the hexagons (e.g., 1 unit)
hex_size = 5

# Generate the hexagonal grid
hexagons = generate_hex_grid(gdf.total_bounds, hex_size)

# Convert the hexagons to a GeoDataFrame
hex_gdf = hex_grid_to_geodataframe(hexagons, gdf.crs)

# Intersect the hexagonal grid with the shapefile to get hexagons within the shape
hex_gdf = hex_gdf[hex_gdf.intersects(gdf.unary_union)]

# Save the hexagonal grid to a new shapefile
hex_gdf.to_file('./output/hex_grid.shp')
