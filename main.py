from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

class WeatherRoot(BoxLayout):
      current_weather= ObjectProperty()
      
      def show_current_weather(self,location= None):
            self.clear_widgets()
            
            if self.current_weather is None:
                  self.current_weather= CurrentWeather()
                  
            if location is not None:
                  self.current_weather.location=location
            
            self.current_weather.update_weather()
            self.add_widget(self.current_weather)
            
      def update_weather(self):
            weather_template="http://api.openweathermap.org/data/2.5/" + "weather?q={},{}&units=metric"
            weather_url=weather_template.format(*self.location)
            request=UrlRequest(weather_url,self.weather_retreived)
            
      def weather_retreived(self,request,data):
            data=json.loads(data.decode()) if not isinstance(data,dict) else data
            self.conditions=data['weather'][0]['description']
            self.temp= data['main']['temp']
            self.temp_min=data['main']['temp_min']
            self.temp_max=data['main']['temp_max']
       
      def show_add_location_form(self):
            self.clear_widgets()
            self.add_widget(AddLocationForm())
      

class AddLocationForm(BoxLayout):
      search_input=ObjectProperty()
      def search_location(self):
          search_template="hhtps://api.openweathermap.org/data/2.5/" + "find?q={}&type=like"
          search_url=search_template.format(self.search_input.text)
          request=UrlRequest(search_url,self.found_location)

      def found_location(self,request,data):
          cities=["{}({})".format(d['name'],d['sys']['country'])
                for d in data['list']]
          self.search_results.item_strings=cities
          self.search_results.adapter.data.clear()
          self.search_results.adapter.data.extend(cities)
          self.search_results.trigger_reset_populate()
      
      def args_converter(self,index,data_item):
            city,country= data_item
            return {'location':(city,country)}
      
class LocationButton(ListItemButton):
     location= ListProperty()

class CurrentWeather(BoxLayout):
      location= ListProperty(['New York','US'])
      conditions=StringProperty()
      temp=NumericProperty()
      temp_min=NumericProperty()
      temp_max=NumericProperty()
      
class WeatherApp(App):
      pass

if __name__=='__main__':
         WeatherApp().run()

