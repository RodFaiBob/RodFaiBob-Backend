import matplotlib
matplotlib.use("Agg")
import os
import matplotlib.pyplot as plt # type: ignore
import matplotlib.animation as animation # type: ignore
last_access_frame = 0

def save_animation(path, nodes, edges, filename):
    global last_access_frame
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
        global last_access_frame

        # Process all skipped frames between last_access_frame and current frame
        new_edges = edges[last_access_frame:frame]

        for i, (src, dest) in enumerate(new_edges):
            edge_index = last_access_frame + i  # Calculate the actual index

            if src in path and dest in path and path.index(dest) - 1 == path.index(src):
                edge_lines[edge_index].set_linestyle('solid')
                edge_lines[edge_index].set_color('black')
                edge_lines[edge_index].set_linewidth(3)
                edge_lines[edge_index].set_zorder(11)
            else:
                edge_lines[edge_index].set_color('blue')
                edge_lines[edge_index].set_linewidth(2)
                edge_lines[edge_index].set_zorder(10)

        last_access_frame = frame  # Update last processed frame
        return edge_lines[last_access_frame:frame]

    writer = animation.FFMpegWriter(fps=20)


    num_frames = 100
    frame_indices = [round(i * (len(edges) - 1) / (num_frames - 1)) for i in range(num_frames)]

    ani = animation.FuncAnimation(fig, update, frames=frame_indices, interval=1, repeat=False)

    dir_path = os.path.dirname(filename) 

    if not os.path.exists(dir_path):
        os.makedirs(dir_path) 
    try:
        ani.save(filename, writer=writer)

    except Exception as e:
        print(f"Error saving file: {e}")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Corrupted file '{filename}' has been removed.")
    last_access_frame = 0
    plt.close(fig) 
    
    

