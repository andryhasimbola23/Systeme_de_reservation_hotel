from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        # Test avec des entiers simples
        label1 = Label(
            text='Test avec taille 18',
            font_size=18,
            color=(0, 0, 0, 1)
        )
        label2 = Label(
            text='Test avec taille 16', 
            font_size=16,
            color=(0, 0, 0, 1)
        )
        layout.add_widget(label1)
        layout.add_widget(label2)
        return layout
if __name__ == '__main__':
    TestApp().run()
