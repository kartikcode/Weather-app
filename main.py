from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.factory import Factory

class WeatherRoot(BoxLayout):
      def show_current_weather(self,location):
            self.clear_widgets()
            current_weather= Factory.CurrentWeather()
            current_weather.location=location
            self.add_widget(current_weather)
       
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

class LocationButton(ListItemButton):
     pass
      
class WeatherApp(App):
      pass

if __name__=='__main__':
         WeatherApp().run()

