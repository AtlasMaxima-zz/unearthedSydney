from scipy.spatial import cKDTree
import numpy as np
import csv

def read_data(input_filename):
    """Read in a file, returning an array and a kdtree"""
    with open(input_filename) as input_file:
        input_reader = csv.reader(input_file)
        data_points = np.array([tuple(map(float,line)) for line in input_reader])
        kdtree = cKDTree(data_points[:,[0,1]])
    return (data_points, kdtree)

def bounds(kdtree):
    """Return the bounds of a kdtree"""
    return (tuple(kdtree.mins), tuple(kdtree.maxes))

def query(data_points, kdtree, queries, resolution):
    """Given the data, a kdtree, a list of points and
    a radius to search in, return a value for each point"""
    return [point_value(data_points[x][:,[2]],data_points,queries[n],kdtree)
            for n,x in enumerate(kdtree.query_ball_point(queries,r=resolution))]

def point_value(arr,data_points,x,kdtree):
    """Get the mean value of a set of points returned from
    a ball query on the kdtree. If there are no points in the radius,
    just return the closest"""
    if len(arr) == 0: return data_points[kdtree.query(x)[1]][2]
    return np.mean(arr)

def grid(data_points, kdtree, xbounds, ybounds, num_xsteps=300, num_ysteps=300):
    """Return a grid of z value between the bounds given"""
    (minx, maxx) = xbounds
    (miny, maxy) = ybounds
    res = np.zeros((num_xsteps,num_ysteps))
    xsteps = np.linspace(minx,maxx,num_xsteps)
    ysteps = np.linspace(miny,maxy,num_ysteps)
    for (i,x) in enumerate(xsteps):
        for (j,y) in enumerate(ysteps):
            res[(i,j)] = query(data_points, kdtree, [(x,y)], max((maxx-minx)/num_xsteps,(maxy-miny)/num_ysteps))[0]
    return (xsteps,ysteps,res)

def draw(xs,ys,zs):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs,ys = np.meshgrid(xs,ys)
    ax.plot_surface(xs,ys,zs)
    plt.show()

def downscale(data_points, kdtree, xbounds, ybounds, num_xsteps=300, num_ysteps=300):
    (xs,ys,data) = grid(data_points, kdtree, xbounds, ybounds, num_xsteps, num_ysteps)
    (xs,ys) = np.meshgrid(xs,ys)
    xs = xs.flatten()
    ys = ys.flatten()
    data = data.flatten()
    new_data = np.array(xs,ys,data).T
    return (new_data, cKDTree(new_data[:,[0,1]]))
