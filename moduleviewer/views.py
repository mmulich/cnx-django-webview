# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response


SITE_TITLE = "Connexions Web View"

def index(request):
    return render_to_response('moduleviewer/index.html',
                              {'title': SITE_TITLE})
