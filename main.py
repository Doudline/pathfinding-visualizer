import gui
import dijkstra
import a_star
import depth_first
import bidirectional_bfs

dij_kstra = dijkstra.Dijkstra()
a__star = a_star.AStar()
depth = depth_first.DepthFirst()
bi_bfs = bidirectional_bfs.BidirectionalBFS()

grid = gui.Gui(dij_kstra, a__star, depth, bi_bfs)
