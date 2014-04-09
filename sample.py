#!/usr/bin/env python
# -*- coding: utf-8 -*-

from muzik import muzik_getter

def sample(muzik_type,muzik_url,delay=True):
    mod = muzik_getter.get(muzik_type)
    if delay:
       mod = getattr(mod ,"delay")
    mod(muzik_url)

if __name__ == "__main__":
    youtube_urls = ["https://www.youtube.com/watch?v=uLiq-A1mR4I","https://www.youtube.com/watch?v=FyXtoTLLcDk","https://www.youtube.com/watch?v=t0--eFfzDAM"]
    soundcloud_urls = ["https://soundcloud.com/sappyfromkobe/swimming-night","https://soundcloud.com/inoranofficial/sets/inoran","https://soundcloud.com/lorenzojovanotti/tensione-evolutiva-musique"]

    print "start soundcloud"
    for s in soundcloud_urls:
        sample("soundcloud",s)

    print "start youtube"
    for y in youtube_urls:
        sample("youtube",y)
