import numpy as np
import matplotlib.pyplot as plt
from glob import *
from scipy.interpolate import interp1d

class plots:
    def __init__(self):
        self.file_names = {}
        self.mst_time = {}
        self.graphs = {}
        self.parse_output()
        self.parse_graph_feature()

    def parse_output(self):
        files = glob("./results/*.txt")
        for file in files:
            name = file.split("rmat")[1].split("_")[0]
            self.file_names[name] = file
            self.mst_time[name] = np.loadtxt(file)

    def parse_graph_feature(self):
        graphs = glob("./data/*.gr")
        for graph in graphs:
            with open(graph, "r") as file:
                content = file.readlines()
            N = int(content[0].split(" ")[0])
            E = int(content[0].split(" ")[1])
            name = graph.split("rmat")[1].split(".")[0]
            self.graphs[name] = {"n": N, "v": E}
        extras = glob("./data/*.extra")
        for extra in extras:
            with open(extra, "r") as file:
                content = file.readlines()
            e = int(content[0])
            name = extra.split("rmat")[1].split(".")[0]
            self.graphs[name]["e"] = e

    def running_time2edges_increase(self):
        mst_time = []
        recompute_time = []
        num_edges = []
        num_nodes = []
        for name, changes in self.mst_time.items():
            edge_num = self.graphs[name]["v"]
            node_num = self.graphs[name]["n"]
            extra = self.graphs[name]["e"]
            weight = changes[:, 0] # weight as edge changes
            running_time = changes[:, 1] # running time as edge changes
            num_edges.append(edge_num)
            num_nodes.append(node_num)
            mst_time.append(running_time[0])
            recompute_time.append(np.sum(running_time[1:]))

        # first graph: plot the running time of static calculation to edge number
        plt.ioff()
        plt.figure()
        plt.plot(num_edges, mst_time, "-o")
        plt.xlabel("original number of edges")
        plt.ylabel("static calculation running time (milliseconds)")
        plt.savefig(r"./static_calculation_running_time.png")
        # second graph: plot the running time of dynamic calculation to edge number
        plt.figure()
        plt.plot(num_edges, recompute_time, "-o")
        plt.xlabel("original number of edges")
        plt.ylabel("dynamic calculation total running time (milliseconds)")
        plt.savefig(r"./dynamic_calculation_total_running_time.png")
        # third graph: plot the running time of static calculation to mlog(n)
        plt.figure()
        plt.plot(num_edges * np.log(num_nodes), mst_time, '-o')
        plt.xlabel("mlog(n)")
        plt.ylabel("static calculation running time (milliseconds)")
        plt.savefig(r"./static_calculation_running_time_mlog(n).png")
        # fourth graph: plot the running time of dynamic calculation to nlog(n)
        plt.figure()
        plt.plot(num_nodes * np.log(num_nodes), recompute_time, "-o")
        plt.xlabel("nlog(n)")
        plt.ylabel("dynamic calculation total running time (milliseconds)")
        plt.savefig(r"./dynamic_calculation_total_running_time_nlog(n).png")

    def main(self):
        self.running_time2edges_increase()


if __name__ == "__main__":
    plotting = plots()
    plotting.main()

