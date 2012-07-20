# -*- coding: utf-8 -*-
import urllib
import urllib2
from urlparse import urljoin, urlparse
from BeautifulSoup import BeautifulSoup
from opensearch import Client as OpenSearchClient
from django.shortcuts import render_to_response


REPO_HOST = 'cnx.org'
REPO_PORT = 80
OPENSEARCH_URL = 'http://%s:%s/opensearchdescription' % (REPO_HOST, REPO_PORT)
SITE_TITLE = "Connexions Web View"

def _fix_url(url):
    """Fix a URL to put to this webview rather than the repository."""
    parts = urlparse(url)
    path = parts.path.split('/')
    if path[1] != 'content':
        # We don't know what this is...
        return url
    id, version = path[:4][-2:]
    path = ['', 'content', '%s@%s' % (id, version)]
    return '/'.join(path)

def index(request):
    return render_to_response('moduleviewer/index.html',
                              {'title': SITE_TITLE})

def search(request):
    client = OpenSearchClient(OPENSEARCH_URL)
    terms = urllib.unquote(request.GET.get('q', '')).decode('utf8')
    results = client.search(terms)
    records = []
    for result in results:
        records.append({'title': result.title,
                        'link': _fix_url(result.link),
                        'summary': result.summary_detail['value'],
                        })
    return render_to_response('moduleviewer/search.html',
                              {'title': SITE_TITLE,
                               'records': records,
                               'search_terms': request.GET.get('q'),
                               })

def module(request, id, version='latest'):
    module_id = id
    module_version = version
    if '@' in module_id:
        module_id, module_version = module_id.split('@')

    # Request the content from the repository.
    url = 'http://%s:%s/content/%s/%s/' % (REPO_HOST, REPO_PORT,
                                          module_id, module_version)
    title = urllib2.urlopen(url + 'Title').read()
    body = urllib2.urlopen(url + 'body').read()

    soup = BeautifulSoup(body)
    # Transform the relative resource links to point to the origin.
    for img in soup.findAll('img'):
        src = img['src']
        if src.startswith('http'):
            continue
        img['src'] = urljoin(url, src)

    # Transform the relative links to point to the correct local
    # address
    for a in soup.findAll('a'):
        href = a.get('href')
        if not href or href.startswith('#') or href.startswith('http'):
            continue
        # Massage the path into this app's URL scheme.
        href = href.rstrip('/')
        path = href.split('/')

        if path[0] != '':
            # Handle resources like .jar files.
            href = urljoin(url, href)
        elif path[1] == 'content':
            # Handles links to other modules.
            version = path.pop()
            href = "%s@%s" % ('/'.join(path), version)
        else:
            # Hopefully everything else falls into this category but
            # I'm doubtful.
            href = urljoin(url, href)
        a['href'] = href

    return render_to_response('moduleviewer/module.html',
                              {'title': SITE_TITLE,
                               'module_title': title,
                               'module_body': str(soup),
                               })
