import time
import gmaps
import cv2
import folium
from folium.plugins import LocateControl
import branca
from branca.element import IFrame
import os
from geopy.geocoders import Nominatim as NT
from matplotlib.transforms import Bbox
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
import folium
from folium.plugins import LocateControl
import matplotlib.pyplot as plt
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarkerPopup,MapMarker

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.app import App
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.clock import Clock

from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from functools import partial
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker, MapSource
import requests
import re
from kivy.lang import Builder

class mapsgoo(Screen):
        def __init__(self,**kwargs):
                super(mapsgoo,self).__init__(**kwargs)
                nhu=BoxLayout(orientation='vertical')
                self.texin=TextInput(text='21.433344',input_filter='float')
                self.texin2=TextInput(text='-89.7654454',input_filter='float')
                
                self.main_map=MapView(lat= 20.9566,lon= -89.6696,zoom=13)
                self.main_map_me=MapMarkerPopup(lat= 20.9566,lon= -89.669,source= 'piedra.png')
                bot1=Button()
                bot1.bind(on_press=self.press)
                bot2=Button(text='agregar marcador')
                bot2.bind(on_press=self.place_pin)
                bot3=Button(text= 'remover marcador')
                bot3.bind(on_press=self.remove_pin)
                #botbefore=Ellipse(angle_start=0,angle_end=360)
                #bot1.add_widget(before)

                #self.main_map_me.add_widget(bot1)
                
                
                self.list_of_lines = []
                self.route_points = []
                self.placed = False
                self.exists = False
                
                #self.main_map.center_on(self.main_map_me.lat, self.main_map_me.lon)
                bbox=BoxLayout(size_hint_y=.1)
                geo1=Button(text='indicaciones',on_press=self.press_dist)
                self.main_map.add_widget(self.main_map_me)
                bbox.add_widget(bot2)
                bbox.add_widget(self.texin)
                bbox.add_widget(self.texin2)
                bbox.add_widget(bot3)
                bbox.add_widget(geo1)
                #self.main_map.add_widget(nhu)
                nhu.add_widget(bbox)
                nhu.add_widget(self.main_map)
                
                self.add_widget(nhu)
                self.contador=1
                


        
        def press(self,*args):
                print(str(self.main_map_me.lat) +  ' | ' + str(self.main_map_me.lon))

        def place_pin(self,*args):
                self.placed = True
                u=float(self.texin.text)
                u2=float(self.texin2.text)
                self.ma='man'+str(self.contador)
                self.ma=MapMarkerPopup(lat= u,lon= u2,source='piedra.png')
                #self.ma.lat=u
                #self.ma.lon=u2
                self.main_map.add_widget(self.ma)
                self.contador+=1


        def remove_pin(self,*args):
                
                
                if self.placed == True:
                        self.main_map.remove_widget(self.d)
                        self.placed = False
                        self.exists = False
                while self.contador>1:                    
                        self.ma='man'+str(self.contador)
                        self.main_map.remove_widget(self.ma)
                        self.contador=1
                self.main_map.remove_widget(self.d)
                
                self.main_map.remove_widget(all)
            
        def on_touch_up(self, touch,*args):
                if touch.y > self.height*0.05:
                        if self.placed == True and self.exists == False:
                                self.d = MapMarkerPopup(lat=self.main_map.get_latlon_at(touch.x, touch.y)[0], lon=self.main_map.get_latlon_at(touch.x, touch.y)[1], source='piedra.png')
                                self.btn = Button(text='como llegar', on_press=self.press_dist)
                                self.d.add_widget(self.btn)
                                self.main_map.add_widget(self.d)
                                print(self.main_map.get_latlon_at(touch.x, touch.y))
                                self.exists = True

        def press_dist(self, instance,*args):
                print(self.d.lat)
                print(self.d.lon)
                self.start_lon = self.main_map_me.lon
                self.start_lat = self.main_map_me.lat
                self.end_lon = self.d.lon
                self.end_lat = self.d.lat
                self.body = {"coordinates":[[self.start_lon,self.start_lat],[self.end_lon,self.end_lat]]}
                self.headers = {
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
	'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
                'Content-Type': 'application/json; charset=utf-8'}
                self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body, headers=self.headers)
                print(self.call.text)
                self.string_res = self.call.text
                print(self.string_res)
                self.tag = 'rtept'
                self.reg_str = '</' + self.tag + '>(.*?)' + '>'
                self.res = re.findall(self.reg_str, self.string_res)
                print(self.res)
                print('_____________________________________')
                self.string1 = str(self.res)
                self.tag1 = '"'
                self.reg_str1 = '"' + '(.*?)' + '"'
                self.res1 = re.findall(self.reg_str1, self.string1)
                print(self.res1)
                for i in range(0, len(self.res1)-1, 2):
                        print('lat= ' + self.res1[i])
                        print('lon= ' + self.res1[i+1])
                        self.points_lat = self.res1[i]
                        self.points_lon = self.res1[i+1]
                        self.points_pop = MapMarkerPopup(lat=self.points_lat, lon=self.points_lon, source='piedra.png')
                        self.route_points.append(self.points_pop)
                        self.main_map.add_widget(self.points_pop)
                with self.canvas:
                        Color(0, 0, 1 ,1)
                        for j in range(0, len(self.route_points)-1, 1):
                                self.lines = Line(points=(self.route_points[j].pos[0],self.route_points[j].pos[1], self.route_points[j+1].pos[0],self.route_points[j+1].pos[1] ), width=4)
                                self.list_of_lines.append(self.lines)

                Clock.schedule_interval(self.update_route_lines, 1/50)
        def update_route_lines(self, *args):
                for j in range(1, len(self.route_points), 1):
                        self.list_of_lines[j-1].points = [self.route_points[j-1].pos[0],self.route_points[j-1].pos[1], self.route_points[j].pos[0], self.route_points[j].pos[1]]


        
class MyApp(App):
    def __init__(self,**kwargs):
        super(MyApp,self).__init__(**kwargs)
    
        self.sm=ScreenManager()
        self.sm.add_widget(mapsgoo(name='p80'))
        
        

    def build(self):
        return self.sm       

MyApp().run()

