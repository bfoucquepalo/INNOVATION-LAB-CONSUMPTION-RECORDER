from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


Builder.load_file('quiz_file_definition.kv')



class SuperTest(TabbedPanel):
    label_wid = ObjectProperty()
    info = StringProperty()
    mycounter = 0
    
    #def build(self):
    #    self.mycounter = 0

    def checkbox_click(self,check,active):
        print(active)

    def myprint(self):
        print('Hello Worlds!!!!!')
        self.mycounter += 1
        self.label_wid.text = 'My label after button press: ' + str(self.mycounter)
        self.info = 'New info text'

class TabbedPanelApp(App):
    def build(self):
        return SuperTest()


if __name__ == '__main__':
    TabbedPanelApp().run()