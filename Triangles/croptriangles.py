# import tkinter
from PIL import Image as PILImage
from PIL import ImageDraw, ImageOps, ImageSequence, ImageStat
import time

def crop(img, mask):
    cropped = ImageOps.fit(img, mask.size, centering=(.5, .5))
    cropped.putalpha(mask)
    # cropped = cropped.crop((0, h/2, w, h))
    # cropped.show()
    return cropped

def getMask(w, h):
    mask = PILImage.new('L', (w, h))
    newData = []
    # mask = mask.convert("RGBA")
    for x in range(w):
        for y in range(h):
            if ((x > w-y) and (x > y)):
                newData.append((255))
            # elif (x > y):
                # newData.append((255, 0, 255, 55))
            else:
                newData.append((0))
    mask.putdata(newData)
    return mask

def getTriangles(j):
    images = []
    s = time.time()
    for i in range(j):
        fname = "gc" + str(i) + ".jpg"
        img = PILImage.open(fname)
        cropped = crop(img, mask)
        # cropped.show()
        new = "quilt/out" + str(i) + ".png"
        cropped = cropped.resize((900, 900))
        cropped.save(new)
        images.append(cropped)
        print("Saved image #{}".format(i))

    o = time.time()

    return images


if __name__ == '__main__':

    # Make mask.
    w, h = 1080, 1080
    mask = getMask(w, h)
    
    ### Process all images
    # images = getTriangles(206)
    '''
    images = []
    for k in range(200):
        fn = "gc" + str(k) + ".jpg"
        img = PILImage.open(fn)
        img = img.resize((300, 300))
        images.append(img)
    print(len(images))
    '''

    ### Make GIF
    # gif = images[0]
    # gif.save("new_resize.gif", format='gif', save_all = True, append_images=images[1:])
    
    '''
    img1 = PILImage.open("out1.png")
    img2 = PILImage.open("out2.png")
    img2.paste(img1, (200, 100), img1)
    img2.show()
    '''

    '''
    images = []
    for k in range(207):
        fn = "out" + str(k) + ".png"
        img = PILImage.open(fn)
        img = img.resize((300, 150))
        images.append(img)
    print("All images resized to 300 x 150.")
    '''
    images = []
    for i in range(206):
        print("Loading image {}".format(i))
        img = PILImage.open("sorted/out"+str(i)+".png")
        images.append(img)
    # new canvas.
    w = 900
    quilt = PILImage.new('LA', (w*5, w*10))

    counter = 0
    imgnum = 0
    x, y = (0, 0)
    # imgdict = []

    for im in images:

        if counter == 0:
            quilt.paste(im, (x, y), im)
        elif counter == 1:
            im = im.rotate(90)
            quilt.paste(im, (x, y), im)

        elif counter == 2:
            im = im.rotate(180)
            quilt.paste(im, (x, y), im)
        elif counter == 3:
            im = im.rotate(270)
            quilt.paste(im, (x, y), im)

        # Reset counter
        counter += 1
        if counter > 3:
            counter = 0
            x += w

            if x >= w*5:
                x = 0
                y += w


        imgnum+=1
    
        # stat = ImageStat.Stat(im)
        # bright = stat.mean[0]
        # imgdict.append((im, bright))

        print("Processed image {}".format(imgnum))

    quilt.show()
    quilt.save("sorted/quilt.png")


    '''

    imgdict.sort(key = lambda x: x[1])

    p = 0
    for imgd in imgdict:
        # print(imgd)
        imgd[0].save("sorted/out"+str(p)+".png")
        print("Saving image {}".format(p))
        p+=1

    '''

    

