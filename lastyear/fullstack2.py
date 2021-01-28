import mutagen

mp4File = mutagen.File(r'/Users/deryck/Downloads/dreambroker_fullstack.mp4')
for name, value in mp4File.tags.items():
    print('{:30} : {}'.format(name, value))
