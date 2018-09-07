
'''
Title: Youtube Comment Retriver

Description: Gets comments and the names of people who commented on a certain
             youtube channel.
Created By:  Bryce Jackson 9/6/2018
'''

import requests
import json

from tkinter import *
from tkinter import ttk

# Define global variables
API_KEY = # FIXME: Enter API-Key
comment_names = []
comments = []

def click(*args):
    link = str(youtube_channel.get())
    print("Your link is:", link)

    link_parts = link.split("/")
    print(link_parts)

    # Arbitraly assign x so it has a higher scope
    # Also, assigns variables
    channelId = "x"

    done = False
    while not done and len(link_parts) > 3:
        if link_parts[3] == "channel":
            channelId = link_parts[4]
            response = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&id=%s&key=%s" % (channelId, API_KEY))
            print('Status Code:', response.status_code)

            json_data = json.loads(response.text)
            channel_name.set(json_data['items'][0]['snippet']['title'])
            done = True

    # FIXME: Add support for diffrent types of links. Example: video links
    done = False
    while not done:
        response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&allThreadsRelatedToChannelId=%s&maxResults=10&key=%s" % (channelId,API_KEY))
        print('Status Code:', response.status_code)

        json_data = json.loads(response.text)

        # Recets global variables
        comment_names =[]
        comments = []
        for i in range(len(json_data['items'])):
            # Appends names from api call
            name = json_data['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_names.append(name)

            # Appends comments from api call
            comment = json_data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment.encode("utf-8"))

        done = True

    # adds text
    for i in range(len(comment_names)):
        print('Doing Stuff')
        ttk.Label(mainframe, text = comment_names[i]).grid(column=1, row=i+6, sticky=(W,E))
        ttk.Label(mainframe, text = comments[i]).grid(column=2, columnspan=2, row=i+6,sticky=(W,E))


# Main Information
window = Tk()
window.title("Get Youtube Comments")

# Frames
mainframe = ttk.Frame(window, padding= "3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Creates input text and buttons
youtube_channel = StringVar()
youtube_channel_entry = ttk.Entry(mainframe, width = 50, textvariable = youtube_channel)
youtube_channel_entry.grid(column = 1, columnspan=3, row = 2, sticky=(W, E))
ttk.Button(mainframe, text="Get Comments", command=click).grid(column=1,row=3, sticky=(W,E))

# Adds labels
channel_name = StringVar()
ttk.Label(mainframe, text = "Youtube Comment Retriver").grid(column=1, columnspan=3, row = 1, sticky= N)
ttk.Label(mainframe, text = "Description: Paste your channel home page or video link and get comments.").grid(column=1, columnspan=3, row=4,sticky= (W,E))
ttk.Label(mainframe, text = "Channel Name:").grid(column=1, row=5,sticky=(W,E))
ttk.Label(mainframe, textvariable = channel_name).grid(column=2, columnspan=2, row=5,sticky=(W,E))

# Adds padding and highlights the entry section
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
youtube_channel_entry.focus()

# Binds enter key to click function
window.bind('<Return>', click)

window.mainloop()
