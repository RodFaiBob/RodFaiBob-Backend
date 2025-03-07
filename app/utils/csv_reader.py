import csv
from app.model.station import Station

STATIONS: dict[str, Station] = {}

def nodeInit(csv_file: str):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        header = next(reader)
        print(f"reading {csv_file} with Header:", ", ".join(header))
        print()

        
        for row in reader:
            try:
                id = row[0].strip()
                name = row[1].strip()
                lat = float(row[2])
                long = float(row[3])
                
                STATIONS[id] = Station(id, name, lat, long)
                
            except Exception as e:
                print(f"Error for row {row}: {repr(e)}")
                
def edgeInit(csv_file: str):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        header = next(reader)
        print(f"reading {csv_file} with Header:", ", ".join(header))
        print()

        
        for row in reader:
            try:
                src_id = row[0].strip()
                dest_id = row[1].strip()
                src = STATIONS[src_id]
                dest = STATIONS[dest_id]

                cost = int(row[2])
                src.addEdge(dest, cost)
                
            except Exception as e:
                print(f"Error for row {row}: {repr(e)}")


        
nodeInit("data/node.csv")
edgeInit("data/edge.csv")