import requests
import json
import random
import os
settings = {}
pos = 0
dlpos = 0
maxc = 0
maxdl = 0
yetToCrawl = []
yetToDl = []
crawled = []
dled = []

def processCMD(cmd):
    global crawled
    global dled
    global help
    global settings
    global maxc
    global maxdl
    global yetToDl
    global yettocrawl


    if cmd.find('help') > -1:
        print('you can: ')
        print('set url (this will be the beginning, starting url)')
        print('set prefix [here] (this is what the program will look for links to the right of)')
        print('set suffix [here] (this is what the program will look for links to the left of up until the prefix)')
        print('set path proxies [here] (this will assume the link to a text file in this directory where proxies are stored, empty means no proxies)')
        print('add dontscrape [here] (adds an item where the program wont scrape or dl if url is containing one of these strings)')
        print('list dontscrape (shows items of dontscrape in an enumerated list)')
        print('rem dontscrape [here] (removes one of the items based on its text)')
        print('clear dontscrape [here] (clears dontscrape list)')
        print('set linkstart (in between parsers, all of your links must start with this to be considered a link, i.e. https\n)')
        print('show linkstart (shows what the current linkstart string is)')
        print('max depth dl [here] (sets the highest amount of files to download{these don\'t get scraped}) cant be 0')
        print('max depth crawl [here] (sets the maximum depth for files to be crawled from) cant be 0')
        print('action start (begins)')
        print('ctrl+c OR ctrl+z (stops the running program')
        print('show settings (shows all the settings')
        print('load settings')
        print('save settings')
        print('add ext (crawl or dl) .exmpl')
        print('rem ext (crawl or dl) here (removes item based on the file extension rather than a number like the other one)')
        print('list ext (crawl or dl) lists ')
        print('save crawled')
        print('save dled')
        print('back')
        print('exit')


    if cmd.find('save cralwed') > -1:
        tpath = os.getcwd() + '/crawled.txt'
        try:
            ou = open(tpath)
            outstr = ''
            for url in crawled:
                outstr += url + '\n'
            ou.write(outstr)
            ou.close()
            print('saved to: ' + os.getcwd() + '/crawled.txt')
        except:
            print('empty set')
    if cmd.find('save dled') > -1:
        tpath = os.getcwd() + '/dled.txt'
        try:
            ou = open(tpath)
            outstr = ''
            for url in dled:
                outstr += url + '\n'
            ou.write(outstr)
            ou.close()
            print('saved to: ' + os.getcwd() + '/crawled.txt')
        except:
            print('empty set')


    if cmd.find('add ext ') > -1:
        subcmd = cmd.split('add ext ')[1]
        if subcmd.find('crawl ') > -1:
            sub2cmd = subcmd.split('crawl ')[1]
            try:
                settings['extcrawl'].append(sub2cmd)
            except:
                settings['extcrawl'] = []
                settings['extcrawl'].append(sub2cmd)

        elif subcmd.find('dl ') > -1:
            sub2cmd = subcmd.split('dl ')[1]
            try:
                settings['crawldl'].append(sub2cmd)
            except:
                settings['crawldl'] = []
                settings['crawldl'].append(sub2cmd)

    if cmd.find('rem ext ') > -1:
        subcmd = cmd.split('rem ext')[1]
        if subcmd.find('crawl ') > -1:
            sub2cmd = subcmd.split('crawl ')[1]
            try:
                settings['extcrawl'].remove(sub2cmd)
                print('Removed: ' + sub2cmd)
            except:
                settings['extcrawl'] = []

        if subcmd.find('dl ') > -1:
            sub2cmd = subcmd.split('dl')[1]
            try:
                settings['crawldl'].remove(sub2cmd)
                print('Removed: ' + sub2cmd)
            except:
                settings['crawldl'] = []

    if cmd.find('list ext ') > -1:
        which1 = cmd.split('list ext ')[1]
        if which1 == 'crawl':
            try:
                print(settings['extcrawl'])
            except:
                print('None')
        elif which1 == 'dl':
            try:
                print(settings['crawldl'])
            except:
                print('None')


    if cmd == 'save settings':
        b = json.dumps(settings)
        lfile = os.getcwd() + '/settings.txt'
        a = open(lfile, 'w')
        a.write(b)
        a.close()

    if cmd.find('set linkstart ') > -1:
        lst = cmd.split('set linkstart ')[1]
        settings['linkstart'] = lst

        print('link start set to: ' + lst)

    if cmd.find('show linkstart') > -1:
        try:
            print(settings['linkstart'])
        except:
            print('none set')

    if cmd == 'load settings':
        try:
            lfile = os.getcwd() + '/settings.txt'
            a = open(lfile)
            b = a.read()
            settings = json.loads(b)
            a.close()
        except Exception as e:
            print(e)

    if cmd == 'show settings':
        try:
            print('max crawl depth: ' + str(settings['maxc']))
            print('max download depth: ' + str(settings['maxdl']))
        except:
            print('max crawl depth or max dl depth not set')
        finally:
            print('other settings: \n')
            print(settings)

    if cmd.find('set url ') > -1:
        urly = cmd.split('set url')[1]
        urly = urly.replace(' ', '')
        settings['url'] = urly

    if cmd.find('set prefix ') > -1:
        try:
            prefix = cmd.split('set prefix ')[1]
            settings['parsers']['prefix'] = prefix
        except:
            settings['parsers'] = {}
            prefix = cmd.split('set prefix ')[1]
            settings['parsers']['prefix'] = prefix

    if cmd.find('set suffix ') > -1:
        try:
            suffix = cmd.split('set suffix ')[1]
            settings['parsers']['suffix'] = suffix
        except:
            settings['parsers'] = {}
            suffix = cmd.split('set suffix ')[1]
            settings['parsers']['suffix'] = suffix

    if cmd.find('clear dontscrape') > -1:
        d = input('are you sure?\n').rstrip()
        if d.startswith('y') or d.startswith('Y'):
            settings['dontscrape'] = []

    if cmd.find('list dontscrape') > -1:
        try:
            print(settings['dontscrape'])
        except Exception as e:
            print(e)

    if cmd.find('add dontscrape ')  > -1:
        try:
            dontscrapes = settings['dontscrape']
            stradd = cmd.split('add dontscrape ')[1]
            dontscrapes.append(stradd)
            settings['dontscrape'] = dontscrapes
        except: ##key error, not found
            dontscrapes = []
            stradd = cmd.split('add dontscrape ')[1]
            dontscrapes.append(stradd)
            settings['dontscrape'] = dontscrapes

    if cmd.find('rem dontscrape ') > -1:
        try:
            item = cmd.split('rem dontscrape ')[1]
            settings['dontscrape'].remove(item)
            print('Removed: ' + item)

        except Exception as err:
            print(err)

    if cmd.find('max depth crawl ') > -1:
        try:
            mc = int(cmd.split('max depth crawl ')[1])
            settings['maxc'] = mc
            print("max crawl depth: " + str(settings['maxc']))
        except Exception as prob:
            print(prob)

    if cmd.find('max depth dl ') > -1:
        try:
            md = int(cmd.split('max depth dl ')[1])
            settings['maxdl'] = md
            print("maximum downloads set to: " + str(settings['maxdl']))
        except Exception as prob:
            print(prob)

    if cmd.find('action start') > -1:
        print('commencing program!\n')
        yetToCrawl.append(settings['url'])
        rcrawl()

    if cmd.find('back') > -1:
        main()

def rcrawl():
    global crawled
    global dled

    global yetToCrawl
    global yetToDl
    global settings
    global maxc
    global maxdl
    global pos
    global dlpos

    ##this one is going to prioritize downloads
    ##check if downloads yet to process:
    if dlpos >= settings['maxdl'] and settings['maxdl'] != 0 and len(yetToDl) > 0:
        yetToDl.clear()
        print('Stopping Downloads, cap reached\n')

    if pos >= settings['maxc'] and settings['maxc'] != 0 and len(yetToCrawl) > 0:
        print('Stopping program, crawl depth reached.\n')
        yetToCrawl.clear()
        return

    if len(yetToDl) > 0 and dlpos < settings['maxdl']:
        urldl = yetToDl.pop(0)
        if urldl.endswith('/'):
            localfile = urldl.split('/')[-1] + 'index'
        else:
            localfile = urldl.split('/')[-1]

        if os.path.isfile(localfile):
            localfile = localfile +  str(random.randrange(1,432345))

        ##download it
        print('downloading: ' + urldl)
        out = dlfile(urldl, localfile)
        dled.append(urldl)
        dlpos += 1
        rcrawl() ##this verifies that it won't crawl more until all files in list are downloaded.
        return
    ##move  on to the crawling instead of downloading,
    if len(yetToCrawl) > 0 and pos < settings['maxc'] and settings['maxc'] != 0:
        urlcrawl = yetToCrawl.pop(0)
        ##get
        print('grabbing page: ' + urlcrawl)
        try:
            req = requests.get(urlcrawl, timeout=30)
            crawled.append(urlcrawl)
        except Exception as e:
            print('Error Retrieving. Code: ' + str(e))
            rcrawl()
            return

        linksfound = []
        if req.ok:
            links1 = req.text.split(settings['parsers']['prefix'])
            for link in links1:
                link2 = link.split(settings['parsers']['suffix'])[0]
                for y in settings['dontscrape']:
                    if link2.find(y) == -1:
                        ##check where to put, downloads or scrapes:
                        #settings['extcrawl'] = list,
                        #settings['crawldl'] = list;
                        #process starting of links:
                        try:
                            lst = settings['linkstart']
                        except:
                            lst = 'Error, must set link start!\n'
                            return
                        ##loops for file extensions
                        for z in settings['extcrawl']:
                            if link2.endswith(z) and link2.startswith(lst) and link2 not in crawled and link2 not in yetToCrawl and link2 != settings['url']:
                                yetToCrawl.append(link2)
                                print('found crawl: ' + link2)

                        for z in settings['crawldl']:
                            if link2.endswith(z) and link2.startswith(lst) and link2 not in dled and link2 not in yetToDl and link2 != settings['url']:
                                yetToDl.append(link2)
                                print('found dl: ' + link2)

            if len(yetToDl) > 0 or len(yetToCrawl) > 0:
                pos += 1
                rcrawl()
                return


def dlfile(url, localname):
    dlspath = os.getcwd() + '/downloads/'
    outpath = dlspath + localname
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dlspath + localname, 'wb') as f:
                for piece in r.iter_content(chunk_size=8192):
                    f.write(piece)
        return('saved to: ' + outpath)
    except Exception as e:
        print(e)

def main():
    global crawled
    global dled

    global settings
    settings['recorddl'] = 'off'
    settings['recordcrawl'] = 'off'
    inp = input('...').rstrip()
    if inp == 'exit':
        quit()
    else:
        crawled = []
        dled = []
        processCMD(inp)
    main()


if __name__ == '__main__':
    a = open(os.getcwd() + '/intro.txt')
    b = a.read()
    print(b)
    a.close()
    main()
