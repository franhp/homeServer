from django.db import models
import os
import re
from collections import Counter
from subprocess import check_output
import string
import shutil


class RPD(models.Model):
    class Meta:
        permissions = (('can_rpd', 'Can enter the rpd section'),)

    def __init__(self, videoPath, thumbnailsPath, downloadsPath):
        self.videoPath = videoPath
        self.thumbnailsPath = thumbnailsPath
        self.downloadsPath = downloadsPath

    def listVideos(self):
        videosPaths = []
        for root, dirs, files in os.walk(self.downloadsPath):
            for name in files:
                videosPaths.append(os.path.join(root, name))
        return videosPaths

    def findMostCommonWords(self):
        # Find filenames
        names = []
        for root, dirs, files in os.walk(self.videoPath):
            for name in files:
                names.append(name)
        # Find most common words in filenames
        words = []
        for name in names:
            for word in re.findall(r'\w+', name):
                if word.upper() not in ('MP4', 'AVI', 'FLV', 'THE') and not word.isdigit() and len(word) > 3:
                    words.append(word.upper())
        return Counter(words).most_common(10)

    def sortVideosByPopularity(self, library, counter):
        videos = []
        thumbnails = []
        
        #List thumbnails
        for root, dirs, files in os.walk(self.thumbnailsPath):
                for f in files:
                    thumbnails.append(f)
        i = 0
        for video in library:
            # Assign rating by popularity
            rating = 0
            for word in re.findall(r'\w+', video):
                for count in counter:
                    if word.upper() == count[0]:
                        rating += count[1]
            # Find thumbnails
            relevantThumbnails = []
            for thumbnail in thumbnails:
                if os.path.basename(video)[:-4] in thumbnail:
                    relevantThumbnails.append(thumbnail)
            # Or create the thumbnails if the video didn't have any
            if len(relevantThumbnails) is 0:
                try:
                    self.createThumbnails(video)
                except Exception, err:
                    print '[%s] is not a video: [%s]' % (video, err)
            i += 1
            videos.append((rating, os.path.basename(video), video, relevantThumbnails, i))

        # Reverse sort the list
        return reversed(sorted(videos))

    def createThumbnails(self, video):
        for i in (5, 50, 250, 500):
            filename = os.path.join(self.thumbnailsPath, os.path.basename(video)[:-4] + '.' + str(i) + '.jpg')
            check_output('ffmpeg  -itsoffset -' + str(i) + '  -i ' + video + ' -vcodec mjpeg -vframes 1 -an -f rawvideo -s 320x240 '+filename, shell=True)

    def fixFilenames(self):
        UGLYCHARS = ''.join(set(string.punctuation) - set('-_+.~%'))
        for root, dirs, files in os.walk(self.videoPath):
            for f in files:
                needsChange = False
                # Check if filename is correct
                for char in f:
                    if char in UGLYCHARS or char is ' ':
                        needsChange = True
                
                if needsChange:
                    newName = []
                    for char in f:
                        if char is ' ':
                            newName.append('.')
                        elif char not in UGLYCHARS:
                            newName.append(char)
                    shutil.move(os.path.join(root, f), os.path.join(root, ''.join(newName)))




