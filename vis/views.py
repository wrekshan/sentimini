from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
import pytz
from django import forms
from random import random, triangular, randint
from django.core import serializers

from django.forms import modelformset_factory
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
# Create your views here.

