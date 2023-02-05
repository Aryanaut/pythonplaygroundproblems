import sys, random, argparse
from PIL import Image, ImageDraw

def createrandomtile(size):
    img = Image.new('RGB', size)

    draw = ImageDraw.Draw(img)
    r = int(min(*size)/100)
    n = 1000

    for i in range(n):
        x, y = random.randint(0, size[0] - r), random.randint(0, size[1] - r)
        fill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse((x-r, y-r, x+r, y+r), fill)

    return img

def createtiledimage(tile, size):
    img = Image.new('RGB', size)
    W, H = size
    w, h = tile.size

    cols = int(W/w) + 1
    rows = int(H/h) + 1

    for i in range(rows):
        for j in range(cols):
            img.paste(tile, (j*w, i*h))

    return img

def createDepthMap(size):
    dmap = Image.new('L', size)
    dmap.paste(10, (200, 25, 300, 125))
    dmap.paste(30, (200, 150, 300, 250))
    dmap.paste(20, (200, 275, 300, 375))
    return dmap

def createShiftedImage(dmap, img):
    assert dmap.size == img.size
    sImg = img.copy()

    pixD = dmap.load()
    pixS = sImg.load()

    cols, rows = sImg.size
    for j in range(rows):
        for i in range(cols):
            xshift = pixD[i, j] / 10
            xpos = i - 140 + xshift
            if xpos > 0 & xpos < cols:
                pixS[i, j] = pixS[xpos, j]

    return sImg

def createStereogram(dmap, tile):
    if dmap.mode is not 'L':
        dmap = dmap.convert('L')

    if not tile:
        tile = createrandomtile((100, 100))

    img = createtiledimage(tile, dmap.size)

    sImg = img.copy()
    pixD = dmap.load()
    pixS = sImg.load()

    cols, rows = sImg.size

    for j in range(rows):
        for i in range(cols):
            xshift = pixD[i, j] / 10
            xpos = i - tile.size[0] + xshift
            if xpos > 0 and xpos < cols:
                pixS[i, j] = pixS[xpos, j]

    return sImg

def main():
    parser = argparse.ArgumentParser(description="Autostereograms...")

    parser.add_argument("--depth", dest="dmfile", required=True)
    parser.add_argument("--tile", dest="tilefile", required=False)
    parser.add_argument("--out", dest="outfile", required=False)

    args = parser.parse_args()

    outfile = 'stereogram.png'
    if args.outfile:
        outfile = args.outfile

    tilefile = False
    if args.tilefile:
        tilefile = args.tilefile

    dmImg = Image.open(args.dmfile)
    asImg = createStereogram(dmImg, tilefile)
    asImg.save(outfile)

if __name__ == "__main__":
    main()