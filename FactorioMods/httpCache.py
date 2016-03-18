import hashlib, os, urllib2, datetime

import logging
logger = logging.getLogger(__name__)


def get_home_dir():
    from os.path import expanduser
    return expanduser("~")


def create_data_dir():
    data_dir = os.path.join(get_home_dir(), ".FactorioMods")
    if not os.path.exists(data_dir):
        logger.info("creating: %s" % data_dir)
        os.mkdir(data_dir)

    return data_dir


def get_md5_str(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def getContent(url):
    logger.debug("url: %s" % url)
    cache_dir = os.path.join(create_data_dir(), "cache")
    # cache_dir = os.path.expanduser("~/.FactorioMods/cache")
    if not os.path.exists(cache_dir):
        logger.info("creating: %s" % cache_dir)
        os.mkdir(cache_dir)

    cache_filename = os.path.join(cache_dir, get_md5_str(url))
    logger.debug("cache_filename: %s" % cache_filename)

    if os.path.exists(cache_filename):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(cache_filename))
        logger.debug("mtime: %s" % mtime)
        mtime_delta = datetime.datetime.now() - mtime
        logger.debug("mtime_delta: %s" % mtime_delta)
        if mtime_delta < datetime.timedelta(minutes=60):
        # if mtime_delta < datetime.timedelta(seconds=10):
            logger.debug("cache hit (time): %s" % url)
            with open(cache_filename, 'r') as f:
                return f.read()

    etag_filename = cache_filename + '.etag'

    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    if os.path.exists(etag_filename):
        with open(etag_filename, 'r') as f:
            etag = f.read()
            logger.debug("request.etag: %s" % etag)
            request.add_header('If-None-Match', etag)

    try:
        response = opener.open(request)

        logger.info("cache miss: %s" % url)
        logger.debug("response.code: %s" % response.getcode())

        etag = response.headers.getheader('etag')
        if etag:

            logger.debug("response.etag: %s" % etag)
            with open(etag_filename, 'w') as f:
                f.write(etag)

        html = response.read()
        with open(cache_filename, 'w') as f:
            f.write(html)
        return html

    except urllib2.HTTPError as e:
        logger.debug("e.code: %s" % e.code)
        if e.code != 304:
            raise
        logger.info("cache hit (http error): %s" % url)
        with open(cache_filename, 'r') as f:
            return f.read()


    # cache_filename = os.path.join(cache_dir, get_md5_str(url))
    # logger.debug("cache_filename: %s", cache_filename)
    # if os.path.exists(cache_filename):
    #     with open(cache_filename, 'r') as f:
    #         return f.read()
    # else:
    #     logger.info("GET %s", url)
    #     response = urllib2.urlopen(url)
    #     html = response.read()
    #     with open(cache_filename, 'w') as f:
    #         f.write(html)
    #
    #     return html
