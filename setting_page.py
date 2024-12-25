from database.models import *
from PyQt5.QtWidgets import  QMessageBox

class SettingPage:
    def __init__(self):
        self.setting_add_page.clicked.connect(self.show_setting_add_page)
        self.setting_delete_page.clicked.connect(self.show_setting_delete_page)
        self.load_setting_page_cb()

    def show_setting_add_page(self):
        self.setting_stack.setCurrentIndex(0)
        self.setting_save_btn.clicked.connect(self.save_setting_add_page_data)
        
    def show_setting_delete_page(self):
        self.setting_stack.setCurrentIndex(1)
        self.setting_delete_btn.clicked.connect(self.delete_setting_delete_page_data)
        self.setting_type_cb.activated.connect(self.load_name_for_delete_page)
        
    def save_setting_add_page_data(self):
        operation_type = self.setting_type_cb.currentData()
        print("operation type = ",operation_type)
        name = str(self.setting_add_name_input.text()).strip()
        if not (name and operation_type):
            QMessageBox.warning(self,"Warning","Name Field is Missing , Please Enter")
            return 0
        print("name=",name)
        if int(operation_type) == 1:
            self.save_class_detail(name)
        elif int(operation_type) == 2:
            self.save_section_detail(name)
            
    def delete_setting_delete_page_data(self):
        operation_type = self.setting_type_cb.currentData()
        id = self.setting_name_cb.currentData()
        if not ( operation_type and id ) :
            QMessageBox.warning(self,"Warning","Some Fields Missing , Please Select")
            return 0
        
        if operation_type == 1:
            self.delete_class_detail(id)
        elif operation_type == 2:
            self.delete_section_detail(id)
        
    
    def load_setting_page_cb(self):
        setting_page_cb_data = {("Class",1),("Section",2)}
        self.setting_type_cb.clear()
        
        for name,id in setting_page_cb_data:
            self.setting_type_cb.addItem(str(name),id)
            
    def save_class_detail(self, class_name : str):
        result = Class.add(name=class_name)
        if result.get("status",None) == "success":
                    self.setting_add_name_input.clear()
                    QMessageBox.information(self, "Info", "Class Record Saved")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    def delete_class_detail(self, class_id : int):
        result = Class.delete(class_id)
        if result.get("status",None) == "success":
                    self.load_name_for_delete_page()
                    QMessageBox.information(self, "Info", "Class Record Deleted")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
        
                    
    def save_section_detail(self, section_name : str):
        result = Section.add(name=section_name)
        if result.get("status",None) == "success":
                    self.setting_add_name_input.clear()
                    QMessageBox.information(self, "Info", "Section Record Saved")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
    def delete_section_detail(self, section_id : int):
        result = Section.delete(int(section_id))
        print("result=",result)
        if result.get("status",None) == "success":
                    self.load_name_for_delete_page()
                    QMessageBox.information(self, "Info", "Section Record Deleted")
        else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
                    
    def load_name_for_delete_page(self):
        operation_type = self.setting_type_cb.currentData()
        if not operation_type:
            QMessageBox.warning(self,"Warning","Please Select Operation Type")
            return 0
        
        if operation_type == 1:
            data = Class.get_names()
        elif operation_type == 2:
            data = Section.get_names()
            
        operation_data= data
        if not operation_data:
            QMessageBox.warning(self,"Warning","Selected Operation not have data")
            return 0
        
        self.setting_name_cb.clear()
        
        for data in operation_data:
            self.setting_name_cb.addItem(str(data.name),int(data.id))
        
        
   

    