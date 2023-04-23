# Breaking into grid 





#### Python script for dividing any shapely polygon into smaller equal sized polygons

import numpy as np
import shapely
from shapely.ops import split
import geopandas 
from shapely.geometry import MultiPolygon, Polygon,LineString
import matplotlib.pyplot as plt
"""
def rhombus(square):
    
    Naively transform the square into a Rhombus at a 45 degree angle
    
    coords = square.boundary.coords.xy
    xx = list(coords[0])
    yy = list(coords[1])
    radians = 1
    points = list(zip(xx, yy))
    Rhombus = Polygon(
        [
            points[0],
            points[1],
            points[3],
            ((2 * points[3][0]) - points[2][0], (2 * points[3][1]) - points[2][1]),
            points[4],
        ]
    )
    return Rhombus
"""

def get_squares_from_rect(RectangularPolygon, side_length=0.0025):
    """
    Divide a Rectangle (Shapely Polygon) into squares of equal area.

    `side_length` : required side of square

    """
    rect_coords = np.array(RectangularPolygon.boundary.coords.xy)
    y_list = rect_coords[1]
    x_list = rect_coords[0]
    y1 = min(y_list)
    y2 = max(y_list)
    x1 = min(x_list)
    x2 = max(x_list)
    width = x2 - x1
    height = y2 - y1

    xcells = int(np.round(width / side_length))
    ycells = int(np.round(height / side_length))

    yindices = np.linspace(y1, y2, ycells + 1)
    xindices = np.linspace(x1, x2, xcells + 1)
    horizontal_splitters = [
        LineString([(x, yindices[0]), (x, yindices[-1])]) for x in xindices
    ]
    vertical_splitters = [
        LineString([(xindices[0], y), (xindices[-1], y)]) for y in yindices
    ]
    result = RectangularPolygon
    for splitter in vertical_splitters:
        result = MultiPolygon(split(result, splitter))
    for splitter in horizontal_splitters:
        result = MultiPolygon(split(result, splitter))
    square_polygons = list(result)

    return square_polygons


def split_polygon(G, side_length=0.025, shape="square", thresh=0.9):
    """
    Using a rectangular envelope around `G`, creates a mesh of squares of required length.
    
    Removes non-intersecting polygons. 
            

    Args:
    
    - `thresh` : Range - [0,1]

        This controls - the number of smaller polygons at the boundaries.
        
        A thresh == 1 will only create (or retain) smaller polygons that are 
        completely enclosed (area of intersection=area of smaller polygon) 
        by the original Geometry - `G`.
        
        A thresh == 0 will create (or retain) smaller polygons that 
        have a non-zero intersection (area of intersection>0) with the
        original geometry - `G` 

    - `side_length` : Range - (0,infinity)
        side_length must be such that the resultant geometries are smaller 
        than the original geometry - `G`, for a useful result.

        side_length should be >0 (non-zero positive)

    - `shape` : {square/rhombus}
        Desired shape of subset geometries. 


    """
    assert side_length>0, "side_length must be a float>0"
    Rectangle    = G.envelope
    squares      = get_squares_from_rect(Rectangle, side_length=side_length)
    SquareGeoDF  = geopandas.GeoDataFrame(squares).rename(columns={0: "geometry"})
    Geoms        = SquareGeoDF[SquareGeoDF.intersects(G)].geometry.values
    if shape == "rhombus":
        Geoms = [rhombus(g) for g in Geoms]
        geoms = [g for g in Geoms if ((g.intersection(G)).area / g.area) >= thresh]
    elif shape == "square":
        geoms = [g for g in Geoms if ((g.intersection(G)).area / g.area) >= thresh]
    return geoms

G=Polygon([(-35.3632620,149.165237),(-35.3588324,149.1628352),(-35.3596148,149.1692911),(-35.3630231,149.1682341)])

#G=Polygon([(-35.36330,149.16581),(-35.36289,149.16475),(-35.36298,149.16475),(-35.36330,149.16581)])
#G=Polygon([(0.,0.),(1.,1.),(2.,1.),(1.,0.),(0.,0.)])
#G=Polygon(overall_list)
#thresh=float(input("Enter the accuracy you want it"))
#side_length=float(input("Enter the side length of the square/rectangles"))
x1,y1 = G.exterior.xy



squares   = split_polygon(G,shape='square',thresh=0.8,side_length=0.00095)

#rhombuses = split_polygon(G,shape='rhombus',thresh=0.5,side_length=0.025)
p = geopandas.GeoSeries(squares)

#p.plot()
#plt.show()




dot=[]
x_center=[]
y_center=[]






for i in range (len(p)):
  
  x,y=p[i].exterior.xy
  
  
  plt.plot(x,y)
  #genrtaes an x coordiante ad y coordinate array list




  #print(x,y)
  x_cord_smrect=[]
  y_cord_smrect=[]
  for j in range (len(x)):
    #proper x_coords/y_coords of each rectangle as an array
    x_cord_smrect.append(x[j])
    y_cord_smrect.append(y[j])
    
  #print("x cordinates of rectangle " + str(x_cord_smrect))
  #print("y coordinates of rectangle"+ str(y_cord_smrect ))
  square_coord=[0,0]
  final_coord_smrect=[0,0,0,0,0]

  for k in range (5):
        # generates (x,y) format of coordinates
        final_coord_smrect[k]=x_cord_smrect[k],y_cord_smrect[k]
  
        #print(final_coord_smrect)

  #print(final_coord_smrect)

  center=list(Polygon(final_coord_smrect).centroid.coords)
  center=np.array(center)
  #print("center is " +str(center))
  
  x_center.append(center[0,0])
  y_center.append(center[0,1])
  
  if (i>0):
    plt.plot([x_center[i-1],x_center[i]],[y_center[i-1],y_center[i]]) 
   
print(dot)
plt.plot(x_center,y_center,'o')
plt.plot(x1,y1)
print(len(x_center))