from PIL import Image
import numpy as np
import argparse

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = "@%#*+=-:. "

def get_average_brightness(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w*h))

def convert_to_ascii(filename, cols, scale, morelevels, invert, map1=gscale2, map2=gscale1):
    global gscale1, gscale2 

    image = Image.open(filename).convert('L')
    W, H = image.size[0], image.size[1]
    print("input image size: %d x %d" % (W, H))
    w = W / cols
    h = w / scale
    rows = int(H/h)

    print("cols %d, rows: %d" % (cols, rows))
    print("tile size: %d x %d" % (w, h))

    if cols > W or rows > H:
        print("Image too small.")
        exit(0)

    aimg = []
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows - 1:
            y2 = H

        aimg.append("")
        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)
            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            avg = get_average_brightness(img)
            if invert:
                avg = 255 - avg

            maplength1 = len(map1) - 1
            maplength2 = len(map2) - 1

            if morelevels:
                gval = map2[int((avg*maplength2)/255)]
            else:
                gval = map1[int((avg*maplength1)/255)]
            
            aimg[j] += gval

    return aimg

def main():
    desc = "This program creates ASCII art."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--filename", dest="filename", required=True)
    parser.add_argument("--scale", dest="scale", required=False)
    parser.add_argument("--outfile", dest="outfile", required=False)
    parser.add_argument("--cols", dest="cols", required=False)
    parser.add_argument("--morelevels", dest="morelevels", action="store_true")
    parser.add_argument("--invert", dest="invert", action="store_true")
    parser.add_argument("--map", dest="mapstr", required=False)

    args = parser.parse_args()

    target = args.filename

    outfile = "ascii.txt"
    if args.outfile:
        outfile = args.outfile

    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    cols = 80
    if args.cols:
        cols = int(args.cols)

    morelevels = False
    if args.morelevels:
        morelevels = args.morelevels

    invert = False
    if args.invert:
        invert = args.invert

    if args.mapstr:
        aimg = convert_to_ascii(target, cols, scale, morelevels, invert, args.mapstr)
    else:        
        aimg = convert_to_ascii(target, cols, scale, morelevels, invert)

    with open(outfile, 'w') as f:
        for row in aimg:
            f.write(row+'\n')
    
    print("%s saved." % outfile)

if __name__ == "__main__":
    main()