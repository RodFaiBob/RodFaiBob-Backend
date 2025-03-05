import os
import matplotlib.pyplot as plt # type: ignore
import matplotlib.animation as animation # type: ignore

def save_animation(path, nodes, edges, folder):
    lats = [station.lat for station in nodes]
    longs = [station.long for station in nodes]

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.scatter(longs, lats, color='blue', label='Stations')

    edge_lines = []
    for src, dest in edges:
        line, = ax.plot([src.long, dest.long], [src.lat, dest.lat], color='gray', linestyle='--')
        edge_lines.append(line)

    for station in nodes:
        ax.text(station.long, station.lat, station.id, fontsize=9, ha='right', zorder=20)

    ax.set_axis_off()
    ax.grid(False)
    
    def update(frame):
        src, dest = edges[frame]
        if src in path and dest in path:
            if path.index(dest) - 1 == path.index(src):
                edge_lines[frame].set_linestyle('solid')
                edge_lines[frame].set_color('black')  
                edge_lines[frame].set_linewidth(3)
                edge_lines[frame].set_zorder(11)
                return edge_lines[frame],
        edge_lines[frame].set_color('blue')
        edge_lines[frame].set_linewidth(2)
        edge_lines[frame].set_zorder(10)
        return edge_lines[frame],


    writer = animation.FFMpegWriter(fps=20)

    ani = animation.FuncAnimation(fig, update, frames=len(edges), interval=100, repeat=False)

    if not os.path.exists(folder):
        os.makedirs(folder)

    ani.save(folder+"/vid.mp4", writer=writer)

    plt.close(fig) 
    

