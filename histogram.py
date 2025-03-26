

from PIL import Image
from pylab import *
import matplotlib.pylab as plt
import matplotlib.pylab as plt2


def rgbhistogram(loc,output):

    im = array(Image.open(loc).convert('RGB'))

    im2 = 255 - im  # invert image green
    im3 = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
    im4 = 255.0 * (im / 255.0) ** 2  # squared blue
    plt2.axis('equal')
    plt2.axis('off')
    plt2.figure()
    plt2.hist(im2.flatten(), 128)
    plt2.hist(im3.flatten(), 128)
    plt2.hist(im4.flatten(), 128)
    plt2.savefig(output+"/rgbhisto.png")


def rgbhistogram2(loc,output):
    im = array(Image.open(loc).convert('RGB'))

    im2 = 255 - im  # invert image green
    im3 = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
    im4 = 255.0 * (im / 255.0) ** 2  # squared blue
    plt2.axis('equal')
    plt2.axis('on')
    plt2.figure()
    plt2.hist(im2.flatten(), 128)
    plt2.hist(im3.flatten(), 128)
    plt2.hist(im4.flatten(), 128)
    plt2.savefig(output+"/rgbhisto2.png")


def redhistogram(loc):
    im = array(Image.open(loc).convert('RGB')) #Opening the image
    im = (100.0 / 255) * im + 100  # clamp to interval 100...200 red
    #Fecthing red pixels
    axis('equal')
    axis('off')
    figure()
    hist(im.flatten(), 128) #Designing the histogram

    show()


def greenhistogram(loc):
    im = array(Image.open(loc).convert('RGB')) #Opening the image
    im = 255 - im  # invert image green #Fecthing green pixels
    axis('equal')
    axis('off')
    figure()
    hist(im.flatten(), 128)#Designing the histogram
    show()


def bluehistogram(loc):
    im = array(Image.open(loc).convert('RGB')) #Opening the image
    im = 255.0 * (im / 255.0) ** 2  # squared blue #Fecthing blue pixels
    axis('equal')
    axis('off')
    figure()
    hist(im.flatten(), 128)#Designing the histogram
    show()

