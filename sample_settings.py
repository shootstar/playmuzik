#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE_PATH = "/tmp/playmuzik"
YOUTUBE_PATH = BASE_PATH + "/youtube/"
SOUNDCLOUD_PATH = BASE_PATH + "/soundcloud/"

ECHO_NEST_API_KEY = ""
SOUNDCLOUD_CLIENT_KEY = ''

# PLAYMUZIK_DATABASE_URL = "postgresql://hajimetakase:@localhost:5432/playmuzik"
PLAYMUZIK_DATABASE_URL = "postgresql+psycopg2:///playmuzik"
youtube_params = {'forceduration': False, 'forcejson': False, 'skip_download': False, 'encoding': None, 'keepvideo': False, 'rejecttitle': None, 'forcethumbnail': False, 'forceformat': False, 'max_filesize': None, 'autonumber_size': None, 'ratelimit': None, 'nooverwrites': False, 'forceurl': False, 'outtmpl': u'%(title)s-%(id)s.%(ext)s', 'nocheckcertificate': False, 'progress_with_newline': False, 'writethumbnail': False, 'forceid': False, 'verbose': False, 'nopart': False, 'noresizebuffer': False, 'bidi_workaround': None, 'usenetrc': False, 'youtube_print_sig_code': False, 'dump_intermediate_pages': False, 'logtostderr': False, 'ignoreerrors': False, 'default_search': None, 'allsubtitles': False, 'writedescription': False, 'include_ads': None, 'writeannotations': False, 'socket_timeout': None, 'test': False, 'writeautomaticsub': False, 'listsubtitles': False, 'download_archive': None, 'age_limit': None, 'min_filesize': None, 'username': None, 'listformats': None, 'youtube_include_dash_manifest': False, 'format': 'bestaudio/best', 'max_downloads': None, 'noprogress': False, 'videopassword': None, 'playlistend': None, 'write_pages': False, 'no_warnings': False, 'proxy': None, 'simulate': False, 'playliststart': 1, 'continuedl': True, 'cookiefile': None, 'password': None, 'max_views': None, 'restrictfilenames': False, 'retries': 10, 'updatetime': True, 'forcetitle': False, 'cachedir': '/home/takase/.cache/youtubde-dl', 'format_limit': None, 'subtitleslangs': [], 'prefer_insecure': None, 'forcefilename': False, 'quiet': False, 'writeinfojson': False, 'prefer_free_formats': False, 'buffersize': 1024, 'prefer_ffmpeg': None, 'writesubtitles': False, 'subtitlesformat': 'srt', 'noplaylist': False, 'debug_printtraffic': False, 'consoletitle': False, 'forcedescription': False, 'min_views': None, 'matchtitle': None}

