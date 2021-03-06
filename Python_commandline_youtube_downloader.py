#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Commandline_youtube_downloader
============================================
Coded By: Jackson Kamya
Email: jacksonkamya48@yahoo.com
This script downloads Music from youtube
Pre-Requirements:
=====================
Python 2.7
BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/download/
pytube: www.pypi.python.org/pypi/pytube/ | www.sourceforge.net/projects/pytube/
Features:
=========
1. Download videos one by one as searched at a prompt
2. Download a list of songs as read line by line from txt file
You are free to copy and modify this script for your own requirements.
"""

import os
import time
from urllib2 import urlopen, Request
import sys

try:
    from bs4 import BeautifulSoup as bs
    from pytube import YouTube
except:
    print('Please install BeautifulSoup and pytube to run this script')
    sys.exit(0)

# creating download folder
base_dir = os.path.expanduser("~")
output_folder = os.path.join(base_dir, "Downloads", "py_cmd_utube_downloads")

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


# Getting youtube search term
def get_search_term():
    while True:
        # line is 92 char long pepify it
        inpt = raw_input('Enter search term\nor press <<Enter>> to change mode: > ').lower()
        if not inpt:
            return main('b')
        # search = inpt.replace(" ", "+")
        # search = '+'.join(srch_terms)
        break
    return inpt.replace(" ", "+")


# downloading the file
def download(url):
    accepted_resolutions = ['480p', '720p', '360p']
    for resol in accepted_resolutions:
        try:
            vid = YouTube(url).get('mp4', resol)
            break
        except Exception:
            if resol not in accepted_resolutions:
                print('No video matching any of the qualities required')
                return False
    vid.download(output_folder)
    return True


# Selecting a file from the list
def select_video(soup):
    video_list = []
    for anchor in soup.findAll('a', href=True, title=True):
        link = anchor['href']
        title = anchor['title']
        if(link[:6] == "/watch"):
            video_list.append((link, title))

    print('=' * 30)
    print('Search Results')
    print('=' * 30)

    if not video_list:
        print('No results found')
        return main(mode)
    count = 0
    for l, t in video_list:
        count += 1
        print(str(count) + " >>> " + t)
    while True:
        try:
            # line 108 char ling pepify it
            selection = int(raw_input('Select from the above list or enter 0 to return to main program > '))
            if(selection > count):
                raise ValueError
            elif(selection == 0):
                return main(mode)
            else:
                return video_list[selection - 1]
        except ValueError:
            # line 92 char long pepify it
            print('Input must be a number in between 1-{}, please try again '.format(count))


# Getting the file
def get_video(soup):
        File = select_video(soup)
        title = File[1]
        link = File[0]
        vid_url = 'https://www.youtube.com' + link
        print('Downloading ' + title)
        try:
            start_time = time.time()
            if download(vid_url):
                end_time = time.time()
                mins = (end_time - start_time) / 60
                secs = (end_time - start_time) % 60
                # line 88 char long pepify it
                print("Downloaded %s in %.0f minutes, %.0f seconds" % (title,mins,secs))
            else:
                print("Could not download the video")
        except Exception as e:
            print(e)
        return


def downloader(term):
    # Openning youtube search page
        try:
            agent = ("Mozilla/5.0 "
                     "(X11; Ubuntu; Linux x86_64; rv:50.0) "
                     "Gecko/20100101 Firefox/50.0")

            url = 'https://www.youtube.com/results?search_query=' + term
            req = Request(url, headers={'User-Agent': agent})
            html = urlopen(req).read()
        except Exception as e:
            print(e)
            return

        # Obtaining page's soup
        try:
            soup = bs(html, "html.parser")
        except Exception as e:
            print(e)
            return

        # Getting the video
        try:
            get_video(soup)
        except Exception as e:
            print(e)
            return


# Selecting mode of operation
def get_mode():
    while True:
        print("A >>> Search videos from the prompt")
        print("B >>> Download videos from a file")
        global mode
        mode = raw_input('Select Mode: A or B > ').lower()
        if len(mode) > 1 or not (mode.startswith('a') or mode.startswith("b")):
            print('Invalid mode, please try again')
            continue
        break
    return mode


# Main function of the program
# passing None seems useless we can pass default mode
def main(m=None):
    if not m:
        mode = get_mode()
    else:
        mode = m
    if(mode == 'a'):
        while True:
            downloader(get_search_term())
    else:
        input_file = raw_input('Provide input file path e.g. D:/input.txt > ')
        if not input_file:
            print("Invalid path, please try again")
            return main(mode)
        else:
            if not os.path.exists(input_file):
                print("File does not exist")
                while True:
                    print("A >> switch mode")
                    print("B >> Try again")
                    print("C >> Quit program")

                    choice = raw_input('Select one of the above options > ')
                    if choice.lower() not in ('a', 'b', 'c'):
                        print('Invalid choice, please try again')
                        continue
                    # can we make it more pythonic ?
                    if(choice == "a"):
                        return main('a')
                    elif(choice == 'b'):
                        return main(mode)
                    else:
                        sys.exit(0)
        with open(input_file, 'r') as f:
            try:
                files = f.readlines()
            except Exception as e:
                print(e)
                return
        for item in files:
            downloader(item.replace(" ", "+"))


if __name__ == "__main__":
    main()
