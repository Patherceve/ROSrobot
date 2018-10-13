import png

def displaypgm(data, width):
    a = []
    w = int(width)
    for i in range(len(data)/w):
        row = [data[x + (i * w)] for x in range(w)]
        a.append(row)
    png.from_array(a, "L").save("out.png")

    
def exportToPNG(data, limit, width, name):
    sys.stdout.write("Exporting")
    a = []
    pixelColor = (255/limit);
    for x in range(0,len(data)):
        if not (x % (width * 5)):
            sys.stdout.write(".")
        a.append(abs((data[x]-1) * pixelColor))
        
    displaypgm(a,width, name)
    print("Exported to: " + name)


