from codecs import Codec
from matplotlib import image
from moviepy.editor import *
from WordTimestamp import WordTimestamp

#Word1 = WordTimestamp(word="cute kittens",start= 0.0,end= 2.4)
#Word2 = WordTimestamp(word="flowers",start= 4,end= 6.5)
#Word3 = WordTimestamp(word="cars",start= 7.0,end= 10.0)

PATHimage = 'C:\\Users\\zorro\\OneDrive\\Documents\\EFREI\\M2\\Projet Transverse\\image\\'
PATH = ''


class ImageXTemp:
    def __init__(self, word, temp):
        self.word = word
        self.temp = temp

##List of WordTimestamp 
Words = []
#Words.append(Word1)
#Words.append(Word2)
#Words.append(Word3)

##List of ImageXTemp of the words with their duration
img = []
LastWordEnd = 0.0
for wts in Words: 
    img.append(ImageXTemp(word= wts.word,temp=(wts.end-LastWordEnd)))
    LastWordEnd = wts.end



##duration=input("Enter video duration:  ") 
name="Username&Title"
#############################################################################
def setDurationImage(img,duration):
    return ImageClip(img).set_duration(duration)

def b2():
    

    clips = [setDurationImage(PATHimage+m.word+".jpg",m.temp) #duration of 1 image
          for m in img]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(PATH+name+".mp4", fps=24,codec = 'mpeg4')

b2()