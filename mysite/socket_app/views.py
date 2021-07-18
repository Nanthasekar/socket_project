from django.shortcuts import render
from .consumers import WSConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from random import randint
from django.http import JsonResponse

# Create your views here.
def index(request):
	return render(request, 'index.html', context={'text':'hello nantha'})

async def home(request):
	# channel_layer = get_channel_layer()
	# await(channel_layer.group_send)(
	# 	"chat_{}".format('12'), {
	# 		'type' : 'send_text',
	# 		'value' : "generated from HOME page"
	# 	}
	# )
	return render(request, 'home.html', context={'text':'hello nantha'})

def second(request):
	return render(request, 'second.html', context={'text':'hello nantha'})

async def test(request):
	idd = request.GET.get('id', '0')
	value = "generated for index page" if int(idd)==12 else "generated for second page"
	cohort_id = 45
	channel_layer = get_channel_layer()
	await(channel_layer.group_send)(
		"chat_{}_{}".format(int(idd), cohort_id), {
			'type' : 'send_text',
			'value' : value
		}
	)
	return JsonResponse({'foo': 'bar'})