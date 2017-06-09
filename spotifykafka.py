from Kafka import KafkaConsumer
import os
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib
from Kafka import KafkaProducer

playlist_consumer = KafkaConsumer('playlists')

r = requests.get('127.0.0.1/access-token')
