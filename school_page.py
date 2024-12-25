from database.models import *
from validator import Validator
from PyQt5.QtWidgets import  QMessageBox
class SchoolPage:
    """
    SCHOOL PAGE - In this class is responsible for School Page , they are :
    1) Class
    2) Section
    3) Subject
    4) Examination
    """
    def __init__(self):
        self.operation_data = {
            "INSERT RECORD" : 1,
            "DELETE RECORD" : 2
        }
        self.information_data = {
            "EXAMINATION" : 1,
            "CLASS" : 2,
            "SECTION" : 3,
            "SUBJECT" : 4
        }
        self.load_information_data()
        self.load_operation()
        self.track_button_to_display_stack_widget()
        pass
    
    def load_information_data(self):
        if not self.information_data:
            print("not found")
            return 0 
        
        for name,id in self.information_data.items():
            self.school_information_cb.addItem(name,id)
    
    def load_operation(self):
        if not self.operation_data:
            print("not found")
            return 0
        
        for name,id in self.operation_data.items():
            self.school_operation_cb.addItem(name,id)
        self.school_operation_cb.setCurrentIndex(-1)
    def track_button_to_display_stack_widget(self):
        information_cb = self.school_information_cb
        operation_cb = self.school_operation_cb
        information_cb.activated.connect(self.display_stack_page)
        operation_cb.activated.connect(self.display_stack_page)
    
    def display_stack_page(self):
        """
        Handling the School Page Stack Container with Operation and Information Item
        """
        information_cb = self.school_information_cb.currentData()
        operation_cb = self.school_operation_cb.currentData()
        
        if not (information_cb and operation_cb):
            return 0
        
        if information_cb == 1: # Examination
            if  operation_cb == 1: # INSERT PAGE
                        self.load_class_and_section(self.school_exam_class_cb,self.school_exam_section_cb)
                        self.school_page_stack_con.setCurrentIndex(0)
                        self.exam_add_btn.clicked.connect(self.save_exam_detail)
            if  operation_cb == 2: # DELETE PAGE
                        self.load_class_and_section(self.school_exam_class_cb_2,self.school_exam_section_cb_2)
                        self.exam_delete_btn.clicked.connect(self.delete_exam_detail)
                        self.listen_class_and_section_obj_for_examination_name(self.school_exam_class_cb_2,self.school_exam_section_cb_2,self.exam_name_cb)
                        self.school_page_stack_con.setCurrentIndex(1)
                        
        elif information_cb == 2: # Class
            if  operation_cb == 1: # INSERT PAGE
                        self.school_page_stack_con.setCurrentIndex(2)
                        self.class_add_btn.clicked.connect(self.save_class_detail)
            if  operation_cb == 2: # DELETE PAGE
                        self.class_delete_btn.clicked.connect(self.delete_class_detail)
                        self.load_name_for_class(self.class_name_cb)
                        self.school_page_stack_con.setCurrentIndex(3)
                        
        elif information_cb == 3: # Section
            if  operation_cb == 1: # INSERT PAGE
                        self.school_page_stack_con.setCurrentIndex(4)
                        self.section_add_btn.clicked.connect(self.save_section_detail)
            if  operation_cb == 2: # DELETE PAGE
                        self.school_page_stack_con.setCurrentIndex(5)
                        self.load_name_for_section(self.section_name_cb)
                        self.section_delete_btn.clicked.connect(self.delete_section_detail)
                        
        elif information_cb == 4: # Subject
            if  operation_cb == 1: # INSERT PAGE
                        self.school_page_stack_con.setCurrentIndex(6)
                        self.load_class_and_section(
                            class_obj = self.school_subject_class_cb,
                            section_obj = self.school_subject_section_cb
                            )
                        self.subject_add_btn.clicked.connect(self.save_subject_detail)
            if  operation_cb == 2: # DELETE PAGE
                        self.school_page_stack_con.setCurrentIndex(7)
                        self.load_class_and_section(
                            class_obj = self.school_subject_class_cb_2,
                            section_obj = self.school_subject_section_cb_2
                            )
                        self.listen_class_and_section_obj_for_subject_name(
                            class_obj = self.school_subject_class_cb_2,
                            section_obj = self.school_subject_section_cb_2,
                            subject_obj = self.subject_name_cb
                        )
                        self.subject_delete_btn.clicked.connect(self.delete_subject_detail)
    
    # EXAMINATION
    def save_exam_detail(self):
        """
        Saving Examination Details on Database.
        """
        examination_name = str(self.exam_name_entry.text()).strip().capitalize()
        class_id = int(self.school_exam_class_cb.currentData())
        section_id = int(self.school_exam_section_cb.currentData())
        
        if not ( examination_name and class_id and section_id):
                QMessageBox.warning(self, "Warning", "Some Field Data Missing !")
                return 0
        
        result = Examination.add(
            name=examination_name,
            class_id=class_id,
            section_id=section_id
        )
        
        
        if result.get("status",None) == "success":
                    self.exam_name_entry.setText('')
                    QMessageBox.information(self, "Info", "Examination Record Saved")
        else:
                    QMessageBox.critical(self, "Warning","Invalid or Already Exists " )
    def delete_exam_detail(self):
        """
        Deleting Exam Detail from Database.
        """
        examination_id : int = self.exam_name_cb.currentData()
        if not examination_id:
            QMessageBox.warning(self, "Warning", " Please Select Class and Section !")
            return 0
        else:
            examination_id = int(examination_id)
            
        result = Examination.delete(examination_id)
        if result.get("status",None) == "success":
                    self.exam_name_entry.setText('')
                    QMessageBox.information(self, "Info", "Examination Record Saved")
        else:
                    QMessageBox.critical(self, "Warning","Invalid or Already Exists " )
    # CLASS
    def save_class_detail(self):
        """
        Saving Class Details on Database.
        """
        class_name : str = str(self.class_name_entry.text()).strip().capitalize()
        if not class_name:
            QMessageBox.warning(self, "Warning", " Some Fields are Missing !")
            return 0
        
        result = Class.add(name=class_name)
        if result.get("status",None) == "success":
                    self.class_name_entry.clear()
                    QMessageBox.information(self, "Info", "Class Record Saved")
        else:
                    QMessageBox.critical(self, "Warning","Invalid or Already Exists " )
    def delete_class_detail(self):
        class_id : int = self.class_name_cb.currentData()
        
        if not class_id:
            QMessageBox.warning(self, "Warning", "  Some Fields are Missing !")
        else:
            class_id = int(class_id)
            
        result = Class.delete(class_id)
        if result.get("status",None) == "success":
                    self.load_name_for_class(self.class_name_cb)
                    QMessageBox.information(self, "Info", "Class Record Deleted")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    # SECTION
    def save_section_detail(self):
        section_name : str = str(self.section_name_entry.text()).strip().upper()
        
        if not section_name:
            QMessageBox.warning(self, "Warning", " Some Fields are Missing !")
            return 0
        
        result = Section.add(name=section_name)
        if result.get("status",None) == "success":
                    self.section_name_entry.clear()
                    QMessageBox.information(self, "Info", "Section Record Saved")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    def delete_section_detail(self):
        section_id : int = int(self.section_name_cb.currentData())
        if not section_id:
            QMessageBox.warning(self, "Warning", " Some Fields are Missing !")
            return 0
        
        result = Section.delete(int(section_id))
        if result.get("status",None) == "success":
                    self.load_name_for_section(self.section_name_cb)
                    self.section_name_cb.setCurrentIndex(-1)
                    QMessageBox.information(self, "Info", "Section Record Deleted")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    # SUBJECT
    def save_subject_detail(self):
        subject_name : str = str(self.subject_name_entry.text()).strip().upper()
        subject_code : str = str(self.subject_code_entry.text()).strip().upper()
        class_id = self.school_subject_class_cb.currentData()
        section_id = self.school_subject_section_cb.currentData()
        
        if not ( class_id and section_id ):
            QMessageBox.warning(self, "Warning", " Please Select Class and Section !")
            return 0
        else:
            class_id = int(class_id)
            section_id = int(section_id)
        
        if not (subject_name and subject_code):
            QMessageBox.warning(self, "Warning", "Some Field Data Missing !")
            return 0
            
        result = Subject.add(
            name=subject_name,
            code=subject_code,
            class_id=class_id,
            section_id=section_id
        )
        if result.get("status",None) == "success":
                    self.subject_name_entry.clear()
                    self.subject_code_entry.clear()
                    QMessageBox.information(self, "Info", "Subject Record Saved")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    def delete_subject_detail(self):
        subject_id : int = int(self.subject_name_cb.currentData())
        if not subject_id:
            QMessageBox.warning(self, "Warning", "Some Field Data Missing !")
            return 0
        result = Section.delete(int(subject_id))
        
        
        if result.get("status",None) == "success":
            self.subject_name_cb.setCurrentIndex(-1)
            QMessageBox.information(self, "Info", "Section Record Deleted")
        else:
            QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    # ANTI REDUNT CODE FUNCTIONS
    def load_name_for_class(self, class_obj : object):
   
        operation_data= Class.get_names()
        if not operation_data:
            QMessageBox.warning(self,"Warning","Selected Operation not have data")
            return 0
        
        class_obj.clear()
        for data in operation_data:
            class_obj.addItem( str(data.name), int(data.id) )
        class_obj.setCurrentIndex(-1)
    
    def load_name_for_section(self, section_obj : object):
        operation_data= Section.get_names()
        if not operation_data:
            QMessageBox.warning(self,"Warning","Selected Operation not have data")
            return 0
        
        section_obj.clear()
        for data in operation_data:
            section_obj.addItem( str(data.name), int(data.id) )
        section_obj.setCurrentIndex(-1)
    def load_name_for_examination(self, examination_obj: object):
        operation_data= Examination.get_names()
        if not operation_data:
            QMessageBox.warning(self,"Warning","Selected Operation not have data")
            return 0
        examination_obj.clear()
        for data in operation_data:
            examination_obj.addItem( str(data.name), int(data.id) )
        examination_obj.setCurrentIndex(-1)
        
    def listen_class_and_section_obj_for_examination_name(self, class_obj, section_obj, examination_obj):
        """
        Loading Examination Name on Combobox by Using current selected Class and Section.
        """
        def load_data():
            class_obj_data = class_obj.currentData()
            section_obj_data = section_obj.currentData()

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
    def listen_class_and_section_obj_for_subject_name(self, class_obj, section_obj, subject_obj):
        """
        Loading Examination Name on Combobox by Using current selected Class and Section.
        """
        def load_data():
            class_obj_data = class_obj.currentData()
            section_obj_data = section_obj.currentData()

            if (class_obj_data != None and class_obj_data >= 0 ) and ( section_obj_data != None and section_obj_data >= 0):
                subject_data = Subject.get_by_class_and_section( class_obj_data, section_obj_data)

                if  subject_data:
                    subject_obj.clear()
                    subject_obj.setEnabled(True)
                    for name,id,code in subject_data:
                        subject_obj.addItem(str(name), id)
                else:
                    subject_obj.clear()
            else:
                pass
            
        class_obj.activated.connect(load_data)
        section_obj.activated.connect(load_data)
    

        
        
            
        
        
    
    
        
        