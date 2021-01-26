# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 12:59:45 2020

@author: g_dic
https://automating-gis-processes.github.io/2016/course-info.html
"""

from shapely.geometry import Point, LineString, Polygon

#points
point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)
point3D = Point(9.26, -2.456, 0.57)

print(point3D)

point_coords = point1.coords
xy = point_coords.xy
print(xy)

point_dist = point1.distance(point2)
print("Distance between the points is {0:.2f} decimal degrees".format(point_dist))


#Linestring
line = LineString([point1, point2, point3])
line2 = LineString([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

# Get x and y coordinates of the line
lxy = line.xy
print(lxy)

l_length = line.length
l_centroid = line.centroid

print("Length of our line: {0:.2f}".format(l_length))
print("Centroid of our line: ", l_centroid)

#Polygon

poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])

print(poly)
print(poly2)


world_exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)]
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]
world = Polygon(shell=world_exterior)
world_has_a_hole = Polygon(shell=world_exterior, holes=hole)

print(world)
print(world_has_a_hole)
print(type(world_has_a_hole))

world_centroid = world.centroid
world_area = world.area
world_bbox = world.bounds
world_ext = world.exterior
world_ext_length = world_ext.length

print("Poly centroid: ", world_centroid)
print("Poly Area: ", world_area)
print("Poly Bounding Box: ", world_bbox)
print("Poly Exterior: ", world_ext)
print("Poly Exterior Length: ", world_ext_length)


#Geometry collections
# Import collections of geometric objects + bounding box
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon, box

multi_point = MultiPoint([point1, point2, point3])
multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

line1 = LineString([point1, point2])
line2 = LineString([point2, point3])
multi_line = MultiLineString([line1, line2])

west_exterior = [(-180, 90), (-180, -90), (0, -90), (0, 90)]
west_hole = [[(-170, 80), (-170, -80), (-10, -80), (-10, 80)]]
west_poly = Polygon(shell=west_exterior, holes=west_hole)
min_x, min_y = 0, -90
max_x, max_y = 180, 90
east_poly_box = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)
multi_poly = MultiPolygon([west_poly, east_poly_box])


print("MultiPoint:", multi_point)
print("MultiLine: ", multi_line)

print("Bounding box: ", east_poly_box)
print("MultiPoly: ", multi_poly)

convex = multi_point.convex_hull
lines_count = len(multi_line)
multi_poly_area = multi_poly.area
west_area = multi_poly[0].area
valid = multi_poly.is_valid

print("Convex hull of the points: ", convex)
print("Number of lines in MultiLineString:", lines_count)
print("Area of our MultiPolygon:", multi_poly_area)
print("Area of our Western Hemisphere polygon:", west_area)
print("Is polygon valid?: ", valid)














