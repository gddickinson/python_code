from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QSpinBox, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

import os
import sys
import time
import re
import random

import pygame

#make sounds folder accessible
parentpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parentpath)

wordCount = 0
timeLimit = 60 #minutes
wordGoal = 0
timeSinceLastWord = 0
thinkingTime = 60


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Write or Affirmation")
        
        self.timerVisible = True
        
        global wordCount
        
        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.wordCount_label = QLabel(self)
        self.wordCount_label.setText('Word Count: {}'.format(wordCount))
        self.status.addPermanentWidget(self.wordCount_label) 
        
        #set window size
        self.resize(1200,700)

        self.timerHide_Action = QAction("Hide Timer", self)
        self.timerHide_Action.setStatusTip("Hide Timer")
        self.timerHide_Action.triggered.connect(self.hideTimer)
        edit_toolbar.addAction(self.timerHide_Action)
        edit_menu.addAction(self.timerHide_Action)        
        
        self.timerStop_Action = QAction("Stop Timer", self)
        self.timerStop_Action.setStatusTip("Stop Timer")
        self.timerStop_Action.triggered.connect(self.stopTimer)
        edit_toolbar.addAction(self.timerStop_Action)
        edit_menu.addAction(self.timerStop_Action)
        
        
        
        
        def wordCountUpdate(text):
            global wordCount, timeSinceLastWord
            
            previousWordCount = wordCount
            
            text = text.lower()
            wordsOnly = re.sub(r"[&!@#$%^&*().<>;:{}\~`+-_=]", '', text)
            wordCount = len(wordsOnly.split())
            self.wordCount_label.setText('Word Count: {}'.format(wordCount))

            if wordCount > previousWordCount:
                timeSinceLastWord = 0

        self.editor.textChanged.connect(lambda: wordCountUpdate(self.editor.document().toPlainText()))        
    
    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Write or Affirmation" % (os.path.basename(self.path) if self.path else "-----"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

    def stopTimer(self):
        stop = QMessageBox.question(self,
                                     "Stop Timer",
                                     "Are you sure want to stop the timer?",
                                     QMessageBox.Yes | QMessageBox.No)
        if stop == QMessageBox.Yes:
            startGUI.stopApp()
            self.timerStop_Action.setVisible(False)
            self.timerHide_Action.setVisible(False)
        return


    def hideTimer(self):
        if self.timerVisible:
            startGUI.clock.hideClock()
            self.timerHide_Action.setText('Show Timer')
            self.timerVisible = False
        else:
            startGUI.clock.showClock()
            self.timerHide_Action.setText('Hide Timer') 
            self.timerVisible = True
        return

    def closeTimerAction(self):
        self.timerVisible = False
        self.timerHide_Action.setText('Show Timer') 

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Are you sure want to quit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            startGUI.stopApp()
            event.accept()
            self.app.quit()
        else:
            event.ignore()

class StartWin(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.qlabel = QLabel(self)
        self.qlabel.setText('How many words do you want to write?')
        
        self.wordCountBox = QSpinBox()
        self.wordCountBox.setRange(0,1000000)
        self.wordCountBox.setValue(1000)
      
        self.qlabel_2 = QLabel(self)
        self.qlabel_2.setText('How long do you want to write for? (min)')
        
        self.timeBox = QSpinBox()
        self.timeBox.setRange(0,10000)
        self.timeBox.setValue(60)          

        self.qlabel_3 = QLabel(self)
        self.qlabel_3.setText('How much thinking time between words? (sec)')
        
        self.thinkingBox = QSpinBox()
        self.thinkingBox.setRange(0,10000)
        self.thinkingBox.setValue(60)  
        
        self.btn = QPushButton("Start",self)
        self.btn.clicked.connect(self.startApp)

        #grid layout
        
        layout = QGridLayout()
        
        #layout.setSpacing(100)      
        layout.addWidget(self.qlabel , 0, 0)
        layout.addWidget(self.wordCountBox, 0, 1)       
        layout.addWidget(self.qlabel_2 , 1, 0)        
        layout.addWidget(self.timeBox, 1, 1)     
        layout.addWidget(self.qlabel_3 , 2, 0)        
        layout.addWidget(self.thinkingBox, 2, 1)                 
        layout.addWidget(self.btn, 3, 1)        
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Write or Affirmation")
        self.show()

    def startApp(self):
        global wordGoal, timeLimit, thinkingTime
        
        wordGoal = self.wordCountBox.value()
        timeLimit = self.timeBox.value()  
        thinkingTime = self.thinkingBox.value()  
        
        self.window = MainWindow()

        self.window.update_title()

        self.window.show()
      
        #self.window.app.exec_()
        
        self.clock = Clock(self)

        self.close()
        return

    def stopApp(self):
        #self.window.close()
        self.clock.stopClock()
        return

class Clock(QWidget):
    def __init__(self, appInstance):
        super().__init__()
        self.initUI()
        
        self.appInstance = appInstance
      
    def initUI(self):
        self.wordGoalReached_Flag = False
        #TODO
        self.clockAlarm = Alarm() #looks like problem with mac version is in Alarm()
        print('ok')  

        layout = QStackedLayout()
        self.iterations = 0
        #Background area test
        self.background = QLabel(self)
        self.background.show()

        #Setup text area for clock
        newfont = QFont("Consolas",60, QFont.Bold)
        self.lbl1 = QLabel()
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl1.setFont(newfont)
        self.lbl1.setWindowFlags(Qt.FramelessWindowHint)
        
        #set background colour using stylesheet
        self.lbl1.setAutoFillBackground(True) # This is important!!
        colourValues = self.getColourValues(0,0,0,0)        
        self.lbl1.setStyleSheet("QLabel { background-color: rgba("+colourValues+"); }") 
               

        #add window title
        self.setWindowTitle("Write or Affirmation - Timer")
        
        #Timer to refresh connection
        self.timer = QTimer(self)
        #timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.updates)
        self.timer.start(1000) #update every 1s
        
        #Start QTime
        self.t = QTime()
        self.t.start()
        
        #run first update
        self.updates()
        
        #layout area for widgets
        layout.addWidget(self.background)
        layout.addWidget(self.lbl1)
        layout.setCurrentIndex(1)
        self.setLayout(layout)
        self.setGeometry(150,150,125,125)
        self.show()

        self.clockAlarm.soundAlarm.connect(self.activateAlarm)


    def getColourValues(self, r,g,b,a):
        color  = QColor(r, g, b)
        alpha  = a
        values = "{r}, {g}, {b}, {a}".format(r = color.red(),
                                             g = color.green(),
                                             b = color.blue(),
                                             a = alpha
                                             )            
        return values
        
    def updates(self):
        global wordGoal, wordCount, timeLimit, timeSinceLastWord
        #update timer display
        #self.showElapsedTime()
        self.showCountdownTime()        
        #update time since last word
        timeSinceLastWord += 1
        
        print(wordCount, wordGoal, int(self.secondsElapsed), int(timeLimit*60), timeSinceLastWord)
        
        #update time    
        self.iterations += 1 #approx 1 iteration/sec
        
        #if wordCount doesn't increase for > 60 seconds trigger alarm
        if timeSinceLastWord > thinkingTime and self.wordGoalReached_Flag == False:
            self.clockAlarm.alarm(1)

        #if timeLimit exceeded trigger alarm
        if self.secondsElapsed > (timeLimit*60) and self.wordGoalReached_Flag == False:
            self.clockAlarm.alarm(2) 
 
        #if wordCount reached trigger completion
        if wordCount > wordGoal and self.wordGoalReached_Flag == False:
            self.wordGoalReached_Flag = True
            self.clockAlarm.alarm(3)            

       
        return
        
    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]
        self.lbl1.setText(text)
 
    def showElapsedTime(self):
        self.secondsElapsed = self.t.elapsed()/1000
        m, s = divmod(self.secondsElapsed , 60)
        h, m = divmod(m, 60)
        
        if h < 10:
            hours = '0'+ str(int(h))    
        else: hours = str(int(h))
            
        if m < 10:
            minutes = '0'+ str(int(m))    
        else: minutes = str(int(m))
        
        if s < 10:
            seconds = '0'+ str(int(s))
        else: seconds = str(int(s))
        
        text = hours + ':' + minutes + ':' + seconds
        #print(text)
        self.lbl1.setText(text)

    def showCountdownTime(self):
        global timeLimit
        self.secondsElapsed = self.t.elapsed()/1000
        
        self.countdown = (timeLimit * 60) - self.secondsElapsed

        if self.countdown >= 0:               
            m, s = divmod(self.countdown , 60)
            
        else:
            m, s = divmod((self.countdown * -1) , 60)  
            colourValues = self.getColourValues(233,1,140,150)        
            self.lbl1.setStyleSheet("QLabel { background-color: rgba("+colourValues+"); }") 
            
        h, m = divmod(m, 60)
        
        if h < 10:
            hours = '0'+ str(int(h))    
        else: hours = str(int(h))
            
        if m < 10:
            minutes = '0'+ str(int(m))    
        else: minutes = str(int(m))
        
        if s < 10:
            seconds = '0'+ str(int(s))
        else: seconds = str(int(s))
        
        text = hours + ':' + minutes + ':' + seconds
        #print(text)
        self.lbl1.setText(text)
    
    def stopClock(self):
        #print('stop')
        #self.t.stop()
        self.timer.timeout.disconnect(self.updates)
        self.timer.stop() 
        self.close()
        self.clockAlarm.stopAllAlarms()
        return

    def hideClock(self):
        self.setVisible(False)
    
    def showClock(self):
        self.setVisible(True)
               
    def closeEvent(self, event):
        self.close()
        startGUI.window.closeTimerAction()

    @pyqtSlot()
    def activateAlarm(value):
        return



class Alarm(QObject):
    ''' Class for creating alarm sounds '''
    soundAlarm = pyqtSignal(int)
 
    def __init__(self):
        # Initialize the alarm as a QObject
        QObject.__init__(self)
        pygame.mixer.init()
        soundFolder = os.path.join(parentpath, 'sounds')
        
        self.alarm_sound_1 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_1.m4a"))
        self.alarm_sound_2 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_2.wav"))   
        self.alarm_sound_3 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_3.wav")) 
        self.alarm_sound_4 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_4.m4a"))
        self.alarm_sound_5 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_5.wav"))   
        self.alarm_sound_6 = pygame.mixer.Sound(os.path.join(soundFolder,"voice_6.wav"))        
        
        self.alarm_sound_7 = pygame.mixer.Sound(os.path.join(soundFolder,"CRASH.wav"))
        self.alarm_sound_8 = pygame.mixer.Sound(os.path.join(soundFolder,"SNROLL_2.wav"))   
        self.alarm_sound_9 = pygame.mixer.Sound(os.path.join(soundFolder,"foghornWAV.wav")) 
        
        
        soundList1 = [self.alarm_sound_1,self.alarm_sound_2,self.alarm_sound_3]
        soundList2 = [self.alarm_sound_4,self.alarm_sound_5,self.alarm_sound_6]
        soundList3 = [self.alarm_sound_7,self.alarm_sound_8,self.alarm_sound_9]
 
    
    def alarm(self, value):
        ''' Sound the Alarm '''
        self.soundAlarm.emit(value)
        
        if value == 1:
            print('alarm 1')
            pygame.mixer.Sound.play(random.choice(soundList1))            
        elif value == 2:
            print('alarm 2')
            pygame.mixer.Sound.play(random.choice(soundList2))            
        elif value == 3:
            print('alarm 3')  
            pygame.mixer.Sound.play(random.choice(soundList3))
 
    def stopAllAlarms(self):
        pygame.mixer.stop()
       

if __name__ == '__main__': 
    startGUI = StartWin()
  

    