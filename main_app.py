from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from instructions import *
from ruffier import *
from kivy.clock import Clock
from kivy.properties import NumericProperty
from seconds import *
from kivy.core.window import Window
from kivy.animation import Animation
from sits import *
from runner import *
name_person = ''
green = (0.40, 0.89, 0, 1)

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

class First(Screen):
    def __init__(self,name = 'first'):
        super().__init__(name = name)

        self.name_person = TextInput(text = '',halign='left',multiline=False,size_hint =(0.4, 0.05),pos_hint={'center_x': 0.6, 'center_y': 0.4})
        global age
        age = TextInput(text = '7',halign='left',multiline=False,size_hint =(0.4, 0.05),pos_hint={'center_x': 0.6, 'center_y': 0.3})
        txt_name = Label(text = 'Введите имя:',size_hint =(.3, .2),pos_hint={'center_x': 0.2, 'center_y': 0.4} ,color = (0, 0, 1, 1))
        txt_age = Label(text = 'Введите возраст:',size_hint =(.3, .2) ,pos_hint={'center_x': 0.2, 'center_y': 0.3}, color = (0, 0, 1, 1))
        btn_next = Button(text = 'Начать',size_hint =(.3, .2),pos_hint={'center_x': 0.5, 'center_y': 0.10}, color = (0, 1, 0, 1), background_color = green)
        instr = Label(text = txt_instruction,pos_hint={'center_x': 0.45, 'center_y': 0.78},color = (0, 1, 0, 1))

        self.add_widget(instr)
        self.add_widget(txt_name)
        self.add_widget(txt_age)
        self.add_widget(btn_next)
        self.add_widget(self.name_person)
        self.add_widget(age)

        btn_next.on_press = self.Btn_Next

    
    def Btn_Next(self):
        try:
            global age
            int(age.text)
            global name_person
            name_person = self.name_person.text
            self.manager.transition.direction = 'left' 
            self.manager.current = 'second'
            
        except:
            error_txt = Label(text = 'Введите число!',size_hint =(.3, .2),pos_hint={'center_x': 0.47, 'center_y': 0.26})
            self.add_widget(error_txt)

class Second(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)

        self.btn_next = Button(text = 'Начать',size_hint =(.3, .2),pos_hint={'center_x': 0.5, 'center_y': 0.10}, color = (0, 1, 0, 1), background_color = green)
        txt_test = Label(text = txt_test1,pos_hint={'center_x': 0.5, 'center_y': 0.5}, color = (0, 1, 0, 1))
        txt_result = Label(text = 'Введите результат:',size_hint =(.3, .2) ,pos_hint={'center_x': 0.2, 'center_y': 0.3},color = (0, 0, 1, 1))
        global result1
        result1 = TextInput(text = '0',halign='left',multiline=False,size_hint =(0.4, 0.05),pos_hint={'center_x': 0.6, 'center_y': 0.3})
        result1.set_disabled(True)
        self.add_widget(txt_test)
        self.add_widget(txt_result)
        self.add_widget(result1)
        self.add_widget(self.btn_next)
        self.add_widget(self.lbl_sec)
        
        self.btn_next.on_press = self.Btn_Next
    
    def sec_finished(self,*args):
        global result1
        self.next_screen = True
        result1.set_disabled(False)
        self.btn_next.set_disabled(False)
        self.btn_next.text = 'Продолжить'

    def Btn_Next(self):
        if not self.next_screen:
            self.btn_next.set_disabled(True)
            self.lbl_sec.start()

        else:
            global result1
            p1 = check_int(result1.text)
            if p1 == False or p1 <= 0:
                error_txt = Label(text = 'Введите число!',size_hint =(.3, .2),pos_hint={'center_x': 0.47, 'center_y': 0.26})
                self.add_widget(error_txt)
            else:   
                self.manager.transition.direction = 'left' 
                self.manager.current = 'third'


class Third(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False

        text = Label(text = 'Выполните 30 приседаний за 45 секунд.',size_hint =(0.5, .1),color = (0, 1, 0, 1))
        self.lbl_sits = Sits(30)
        self.run = Runner(total = 30, steptime = 1.5,size_hint=(0.4, 1))
        self.run.bind(finished = self.run_finished)

        line = BoxLayout()
        vlay = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        vlay.add_widget(self.lbl_sits)
        line.add_widget(text)
        line.add_widget(vlay)
        line.add_widget(self.run)

        self.btn_next = Button(text = 'Начать',size_hint =(.3, .2),pos_hint={'center_x': 0.5, 'center_y': 0.10},color = (0, 1, 0, 1), background_color = green)                
        self.btn_next.on_press = self.Btn_Next

        outer = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        outer.add_widget(line)
        outer.add_widget(self.btn_next)
        self.add_widget(outer)

    def run_finished(self, instance, value):
        self.btn_next.set_disabled(False)
        self.btn_next.text = 'Продолжить'
        self.next_screen = True

    def Btn_Next(self):
        if not self.next_screen:
            self.btn_next.set_disabled(True)
            self.run.start()
            self.run.bind(value = self.lbl_sits.next)
        else:
            self.manager.transition.direction = 'left' 
            self.manager.current = 'fourth'

class Fourth(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)
        self.stage = 0

        text = Label(text = txt_test3,pos_hint={'center_x': 0.5, 'center_y': 0.6},color = (0, 1, 0, 1))
        global result2
        global result3
        result2 = TextInput(text = '0',halign='left',multiline=False,size_hint =(0.4, 0.05),pos_hint={'center_x': 0.6, 'center_y': 0.4})
        result3 = TextInput(text = '0',halign='left',multiline=False,size_hint =(0.4, 0.05),pos_hint={'center_x': 0.6, 'center_y': 0.3})
        result2.set_disabled(True)
        result3.set_disabled(True)
        self.do = Label(text = 'Замеряйте пульс в течении 15-и секунд!',size_hint =(.3, .2),pos_hint={'center_x': 0.5, 'center_y': 0.9})
        txt_result1 = Label(text = 'Результат:',size_hint =(.3, .2),pos_hint={'center_x': 0.2, 'center_y': 0.4} ,color = (0, 0, 1, 1))
        txt_result2 = Label(text = 'Результат после отдыха:',size_hint =(.3, .2) ,pos_hint={'center_x': 0.2, 'center_y': 0.3},color = (0, 0, 1, 1))
        self.btn_next = Button(text = 'Начать',size_hint =(.3, .2),pos_hint={'center_x': 0.5, 'center_y': 0.10},color = (0, 1, 0, 1), background_color = green)

        self.add_widget(self.do)
        self.add_widget(text)
        self.add_widget(result2)
        self.add_widget(result3)
        self.add_widget(self.btn_next)
        self.add_widget(txt_result1)
        self.add_widget(txt_result2)
        self.add_widget(self.lbl_sec)
        self.error_txt1 = Label(text = '',size_hint =(.3, .2),pos_hint={'center_x': 0.47, 'center_y': 0.35})
        self.add_widget(self.error_txt1)

        self.error_txt2 = Label(text = '',size_hint =(.3, .2),pos_hint={'center_x': 0.47, 'center_y': 0.26})
        self.add_widget(self.error_txt2)

        self.btn_next.on_press = self.Btn_Next

    def sec_finished(self,*args):
        if self.lbl_sec.done:
            if self.stage == 0:
                self.stage = 1
                self.do.text = 'Отдыхайте 30 секунд!'
                self.lbl_sec.restart(30)
                global result2
                result2.set_disabled(False)
            
            elif self.stage == 1:
                self.stage = 2
                self.do.text = 'Замеряйте пульс в течении 15-и секунд!'
                self.lbl_sec.restart(15)
            
            elif self.stage == 2:
                global result3
                result3.set_disabled(False)
                self.btn_next.set_disabled(False)
                self.btn_next.text = 'Завершить'
                self.next_screen = True


    def Btn_Next(self):
        if not self.next_screen:
            self.btn_next.set_disabled(True)
            self.lbl_sec.start()

        else:
            ok1 = False
            ok2 = False
            self.error_txt1.text = ''
            self.error_txt2.text = ''
            
            global result2
            p2 = check_int(result2.text)
            if p2 == False or p2 <= 0:
                self.error_txt1.text = 'Введите число!'
            
            else:
                ok1 = True

            global result3
            p3 = check_int(result3.text)
            if p3 == False or p3 <= 0:
                self.error_txt2.text = 'Введите число!'

            else:
                ok2 = True

            if ok1 == True and ok2 == True:
                self.manager.transition.direction = 'left' 
                self.manager.current = 'fifth'

class Fifth(Screen):
    def __init__(self,name='fifth'):
        super().__init__(name = name)
        self.instr = Label(text = '',color = (1, 0, 0, 1))
        self.add_widget(self.instr)
        self.on_enter = self.before
    
    def before(self):
        global name_person
        self.instr.text =  name_person +'\n' + test(result1,result2,result3,age)

class HeartCheckApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(First())
        sm.add_widget(Second(name = 'second'))
        sm.add_widget(Third(name = 'third'))
        sm.add_widget(Fourth(name = 'fourth'))
        sm.add_widget(Fifth())
    

        return sm

HeartCheckApp().run()