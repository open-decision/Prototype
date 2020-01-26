from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
import json
from dashboard.views import build_tree
from dashboard.models import DecisionTree
from django.contrib.auth.decorators import login_required
from builder.forms import NodeFormVisualBuilder



def visualbuilder_view(request):
    context = {}
    return render(request, 'visualbuilder.html', context)

def load_node_form(request):
    if request.method == 'GET':
        node_form = NodeFormVisualBuilder
        context = {
        'form': node_form,
        }
        return render(request, 'node_form.html', context)