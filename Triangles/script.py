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
        new = "print/fix" + str(i) + ".png"
        cropped = cropped.resize((900, 900))
        cropped.save(new)
        images.append(cropped)
        print("Saved image #{}".format(i))

    o = time.time()

    return images

def quilted(i_array, w= 432, sp= 50):
    quilt = PILImage.new('LA', (w*6 + sp*6 + sp, w*9 + sp*9 + sp))

    
    counter = 0
    imgnum = 0
    x, y = (sp, sp)

    for im in i_array:
        
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
            x += w + sp

            if x >= w*6:
                x = sp
                y += w + sp
        imgnum += 1
        print(imgnum)

    return quilt

def saveSorted(i_array):
    imgdict = []
    imgnum = 0
    for im in images:
        imgnum+=1
    
        stat = ImageStat.Stat(im)
        bright = stat.mean[0]
        imgdict.append((im, bright))

        print("Processed image {}".format(imgnum))

    imgdict.sort(key = lambda x: x[1])

    p = 0
    for imgd in imgdict:
        # print(imgd[1])
        # print(imgd)
        imgd[0].save("half/sorted"+str(p)+".png")
        print("Saving sorted image #{}".format(p))
        p+=1


    return imgdict

def quilted_alt(images):

    for j in range(0, 104,2):
        im = images[j]
        print(j)
        quilt.paste(im, (x, y), im)

        im = images[210 - j - 1]
        print(j+1)
        im = im.rotate(90)
        quilt.paste(im, (x, y), im)


        im = images[j + 1]
        print(200-j)
        im = im.rotate(180)
        quilt.paste(im, (x, y), im)

        im = images[210 - j - 1]
        print(200-j-1)
        im = im.rotate(270)
        quilt.paste(im, (x, y), im)

        x += w + sp

        if x >= w*6:
            x = sp
            y += w + sp
        imgnum += 1

def getGIF(i_array, name):
    gif = i_array[0]
    gif.save(name +".gif", format='gif', save_all = True, append_images=i_array[1:])


def split(i_array):
    w = 432
    h = 432
    counter = 0
    for img in i_array:
        # img.open()
        print("Splitting image {}".format(counter))
        fn_l = "half/" + str(counter) +"out_l.png"
        fn_r = "half/" + str(counter) +"out_r.png"
        l = img.crop((0, h/2, w/2, h))
        r = img.crop((w/2, h/2, w, h))
        l.save(fn_l)
        r.save(fn_r)
        counter += 1
        # img.close()


if __name__ == '__main__':

    # Make mask.
    w, h = 900,900
    mask = getMask(w, h)
    
    ### Process all images
    # o_images = getTriangles(8)

    # images = []
    # for k in range(1,439):
    #     print("Opening image " + str(k))
    #     fn = "half/out" + str(k) + ".png"
    #     img = PILImage.open(fn)
    #     img.load()
    #     # img = img.resize((432,432))
    #     images.append(img)


    # print(len(images))

    # sort = saveSorted(images)
    # quilt = quilted(images,w= 432, sp= 0)
    # quilt.show()
    # quilt.save("print/print.png")

    # split(images)
    # sp = 0 
    # w = 432
    # quilt = PILImage.new('LA', (w*6 + sp*6 + sp, w*9 + sp*9 + sp))
    # counter = 0
    # imgnum = 0
    # x, y = (sp, sp)
    # # print("Starting pasting.")
    l_c = 0
    r_c = 0
    for i in range(400):
        test = PILImage.open("half/sorted"+str(i)+".png")

        r, g, b, L =  test.getpixel((5,205))
        r, g, b, R = test.getpixel((210, 205))
        
        if L == 0 and R == 0:
            print("Hmm... " + i)
        elif L!=0 and R != 0:
            print("Both visible..." + i)
        elif L != 0:
            print("This image is a LEFT image.")
            test.save("half/left/out"+str(l_c)+".png")
            l_c += 1
        elif R != 0:
            print("This image is a RIGHT image.")
            test.save("half/right/out"+str(r_c)+".png")
            r_c += 1
    # quilt.show()



    

