import numpy as np
import PIL.Image as Image
import argparse
import os
import imghdr
import random

def getAvRGB(img):
    im = np.array(img)
    w, h, d = im.shape
    return tuple(np.average(im.reshape(w*h, d), axis=0))

def splitImg(img, size):
    W, H = img.size[0], img.size[1]
    m, n = size
    w, h = int(W/n), int(H/m)

    imgs = []

    for j in range(m):
        for i in range(n):
            imgs.append(img.crop((i*w, j*h, (i+1)*w, (j+1)*h)))

    return imgs

def get_best_match(input_avg, avgs):
    avg = input_avg
    index = 0
    min_index = 0
    min_dist = float("inf")
    for val in avgs:
        dist = ((val[0] - avg[0])*(val[0] - avg[0]) +
                (val[1] - avg[1])*(val[1] - avg[1]) +
                (val[2] - avg[2])*(val[2] - avg[2]))

        if dist < min_dist:
            min_dist = dist
            min_index = index

        index += 1

    return min_index

def getImages(dir):
    files = os.listdir(dir)
    images = []
    count = 0
    nfiles = len(files)
    for file in files:
        filePath = os.path.abspath(os.path.join(dir, file))
        try:
            f = open(filePath, 'rb')
            img = Image.open(f)
            images.append(img)
            img.load()
            f.close()
            count += 1
            print('%d of %d images loaded' % (count, nfiles))
        except:
            print("invalid image. %s" % (filePath))

    return images

def getFilenames(dir):
    files = os.listdir(dir)
    filenames = []
    for file in files:
        filePath = os.path.abspath(os.path.join(dir, file))
        try:
            imgType = imghdr.whatType(filePath)
            if imgType:
                filenames.append(filePath)
        except:
            print("invalid image. %s" % (filePath))

    return filenames

def create_grid(images, dimensions):
    m, n = dimensions

    assert m*n == len(images)

    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    grid_img = Image.new('RGB', (n*width, height*m))

    for index in range(len(images)):
        row = int(index/n)
        col = index - n*row
        grid_img.paste(images[index], (col*width, row*height))

    return grid_img

def create_mosaic(target, input_images, grid_size, reuse=False):

    targets = splitImg(target, grid_size)

    output = []
    count = 0
    batch_size = int(len(targets)/10)

    avgs = []
    for img in input_images:
        avgs.append(getAvRGB(img))

        print("processed %d of %d..." % (count, len(targets)))

        count += 1

    count = 0

    for img in targets:
        avg = getAvRGB(img)

        match_index = get_best_match(avg, avgs)
        output.append(input_images[match_index])

        if count > 0 and batch_size > 0 and count % batch_size == 0:
            print("processed %d of %d..." % (count, len(targets)))

        count += 1
        if not reuse:
            input_images.remove(match_index)

    print('creating mosaic...')
    mosaic = create_grid(output, grid_size)
    return mosaic

def main():
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    # add arguments
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--reuse-images', dest='reuse_images', required=False)
    parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)
    args = parser.parse_args()

    target = Image.open(args.target_image)
    input_images = getImages(args.input_folder)

    if input_images == []:
        print("No images found in %s. Exiting." % (args.input_folder, ))
        exit()

    random.shuffle(input_images)
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

    output_filename = 'mosaic.png'
    if args.outfile:
        output_filename = args.outfile

    reuse_images = True
    resize_input = True

    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
            print('grid size less than number of images')
            exit()

    if resize_input:
        dimensions = (int(target.size[0]/grid_size[1]), int(target.size[1]/grid_size[0]))
        print("max tile dimensions: %s" % (dimensions, ))
        
        for img in input_images:
            img.thumbnail(dimensions)

    print("Creating Mosaic...")

    mosaic = create_mosaic(target, input_images, grid_size, reuse_images)
    mosaic.save(output_filename, "PNG")
    print('done.')

if __name__ == '__main__':
    main()