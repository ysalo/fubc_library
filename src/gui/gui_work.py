import kivy 
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.button import Label

class TutorialApp(App):
    
    def build(self):
        return Label()

tut = TutorialApp()
tut.run()