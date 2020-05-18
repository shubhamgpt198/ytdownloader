from django.shortcuts import render
from django.http import HttpResponse
import youtube_dl


def index(request):
    return render(request, 'index.html') 

def download(request):
    if request.method == 'POST':
        video_url = request.POST.get('textfield')

    ydl_opts = {'title': '', 'thumbnail':'','hour':'', 'min':'' ,'sec': '', 'formats':{}}

    with youtube_dl.YoutubeDL() as ydl:
        meta = ydl.extract_info(video_url, download=False) 
        formats = meta['formats']
    
    #print(formats)
    formt = {}
    for i in formats:
        if(i['format_note'] == 'tiny'):
            format_note = 'Audio Only'
        else:
            format_note = i['format_note']
        if(i['format_id'] == '17' or i['format_id'] == '36' or i['format_id'] == '18' or i['format_id'] == '22' or i['format_id'] == '137'  ):
            if(type(i['filesize']) == int):
                filesize = int(i['filesize'])/1048576
                filesize = round(filesize,2)
            else:
                filesize = '0'
            formt.update({format_note : [i['url'], filesize]})
    
    
    title = meta['title']
    thumbnail = meta['thumbnail']
    duration = meta['duration']
    hours = int(int(duration)/3600)
    if(hours<10):
        hour = '0' + str(hours)
    else:
        hour = str(hours)
    minutes = int((int(duration)%3600)/60)
    if(minutes<10):
        minute = '0' + str(minutes)
    else:
        minute = str(minutes)
    seconds = (duration%3600)%60
    if(seconds<10):
        second = '0' + str(seconds)
    else:
        second = str(seconds)
    ydl_opts['hour'] = hour
    ydl_opts['min'] = minute
    ydl_opts['sec'] = second
    ydl_opts['formats'] = formt 
    ydl_opts['title']= title
    ydl_opts['thumbnail'] = thumbnail
    ydl_opts['duration'] = duration
    #print(ydl_opts)

    return render(request, 'download.html',ydl_opts)

	