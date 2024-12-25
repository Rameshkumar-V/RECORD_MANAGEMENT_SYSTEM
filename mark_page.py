from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QWidget

from PyQt5.QtWidgets import  QMessageBox
from database.models import *

class MarksPage:
    def __init__(self):
        self.subjects=[]
        self.current_student_mark={}
        self.markpage_add_btn.clicked.connect(self.save_marks_to_db)
        self.mark_class_cb.activated.connect(self.load_data)
        self.mark_section_cb.activated.connect(self.load_data)

    def save_marks_to_db(self):
        student_id = self.mark_register_no_cb.currentData()
        examination_id= self.mark_page_examination_cb.currentData()
        if not student_id and not examination_id:
            QMessageBox.warning(self, "Warning", "Invalid Data,Student Or Examination is Missing ! ")
            return 0

        data_for_db = []
        # print("current student mark = ",self.current_student_mark.items())

        for subject_id,mark in self.current_student_mark.items():
           
            try:
                data_for_db.append({
                    "student_id": int(student_id),
                    "subject_id": int(subject_id),
                    "mark": int(mark.text()),
                    "examination_id": int(examination_id)

                })
            except Exception as e:
                print("error=",e)
                QMessageBox.warning(self, "Error", f"Invalid Data,check Your Data ! {e}")
                return 0
            finally:
                data_for_db.clear()
            
        if data_for_db and len(data_for_db)>=1:
            result = StudentMarks.add_from_list(data_for_db)

            if result.get("status")=="success":
                QMessageBox.information(self, "Info", "Record Saved")
            else:
                QMessageBox.critical(self, "Error", f"Unable to Save error :  ")

        else:
            QMessageBox.warning(self, "Warning", "Invalid Data,check Your Data ! ")
            return 0
    
    
        
    def load_data(self):
            print("LOADING DATA.....................")
            class_obj_data = self.mark_class_cb.currentData()
            section_obj_data = self.mark_section_cb.currentData()
            
            # Loading Subject Form
            if not (class_obj_data and section_obj_data):
                return 0 
            self.load_subject_form(class_obj_data,section_obj_data)
            print("LOADING SUBJECT FORM ................")

            if (class_obj_data != None and class_obj_data >= 0 ) and ( section_obj_data != None and section_obj_data >= 0):
                examination_data = Examination.get_by_class_and_section( class_obj_data, section_obj_data)

                if  examination_data:
                    self.mark_page_examination_cb.clear()
                    self.mark_page_examination_cb.setEnabled(True)
                    for name,id in examination_data:
                        self.mark_page_examination_cb.addItem(str(name), id)
                else:
                    self.mark_page_examination_cb.clear()
            else:
                pass
    # LOADING REGNO WITH CLASS AND SECTION FOR ALL UI
    def cb_event_listner_to_load_examination_name(self, class_obj, section_obj, examination_obj):
        print("EVENT LISTENER")
        def load_data():
            print("LOADING DATA.....................")
            class_obj_data = class_obj.currentData()
            section_obj_data = section_obj.currentData()
            # Loading Subject Form
            # self.load_subject_form(class_obj_data,section_obj_data)

            if (class_obj_data != None and class_obj_data >= 0 ) and ( section_obj_data != None and section_obj_data >= 0):
                examination_data = Examination.get_by_class_and_section( class_obj_data, section_obj_data)

                if  examination_data:
                    examination_obj.clear()
                    examination_obj.setEnabled(True)
                    for name,id in examination_data:
                        examination_obj.addItem(str(name), id)
                else:
                    examination_obj.clear()
            else:
                pass
        
            
        class_obj.activated.connect(load_data)
        section_obj.activated.connect(load_data)
    def clear_layout(self, layout : object):
        while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        
    

    def load_subject_form(self, class_data, section_data):
        print("LOADING SUBJECT FORM")
        # Setting Scroll Widget
        scroll_content = self.student_marks_scroll.widget()
        if scroll_content is None:
            scroll_content = QWidget()
            self.student_mark_scroll.setWidget(scroll_content)
            scroll_content.setLayout(QGridLayout())
        # Setting Layout
        layout = scroll_content.layout()
        if layout is None:
            layout = QGridLayout()
            scroll_content.setLayout(layout)
        self.clear_layout(layout)
        
        # Adding Subjects
        self.current_student_mark={}
        self.current_student_mark.clear()
        self.subjects=Subject.get_by_class_and_section(class_data,section_data)
        
        
        if self.subjects and len(self.subjects)>=1:
            for i in range(len(self.subjects)):
                label = QLabel(f"Subject {self.subjects[i].name }")
                entry = QLineEdit()

                label.setMaximumWidth(150)
                
                label.setStyleSheet("font-size: 22px;")
                label.setFixedSize(300, 60)
                entry.setFixedSize(300, 50)
                entry.setStyleSheet("background-color: rgb(255, 255, 255);border-radius : 8px;border-color: rgb(0, 0, 0);border: 1px solid black")
                self.current_student_mark[self.subjects[i].id]=entry

                layout.addWidget(label, i, 0)
                layout.addWidget(entry, i, 1)
                
        else:
            
            self.clear_layout(layout)
    



    





