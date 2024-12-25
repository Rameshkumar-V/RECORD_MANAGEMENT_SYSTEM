
from database.models import *
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtWidgets import QFileDialog,QListWidget,QListWidgetItem
import pandas as pd
class ReportPage:
    def __init__(self):
        
        self.informations = { ( "All Student Information", 1), ("Student Adhaar Information", 2) ,( "Student Bank Information", 3),( "Student Mark Information" , 4) }
        self.file_types = { ("Excel",1), ("Word Docx",2)}
        self.load_class_and_section(self.report_class, self.report_section)
        self.report_export_btn.clicked.connect(self.__student_detail)
        self.report_progress.setVisible(False)
        self.columns = ["Id", "Register No", "Name", "Date of Birth", "Email Id", "Address", 
            "Contact No", "Ration Card No", "Community", "Adharr No", 
            "Account No", "Bank Name", "Branch Name", "IFSC Code", "MICR Code"
            ]
        self.__type_data= {
            "STUDENT": 1,
            "EXAMINATION" : 2
            
        }
        self.load_type_cb()
        self.__load_information_for_columns()
        # self.__load_file_types()
        self.__display_stack_handler
        self.report_type_cb.activated.connect(self.__display_stack_handler)

    def __load_examination_page_data(self):
        self.load_class_and_section(self.report_mark_class_cb,self.report_mark_section_cb)
        self.cb_event_listner_to_load_examination_name(self.report_mark_class_cb,self.report_mark_section_cb,self.report_exan_type_cb)
        self.__load_file_types(self.report_mark_file_type)
        
    def __load_information_for_columns(self):
        # User Select they wanted columns.
        print(self.columns)
        items = self.columns
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setCheckState(False)
            self.report_columns.addItem(item)
        self.__load_file_types(self.report_file_type)
        
            
    def load_type_cb(self):
        for name,id in self.__type_data.items():
            self.report_type_cb.addItem(str(name),int(id))
        
    def __display_stack_handler(self):
        type : int = int(self.report_type_cb.currentData())
        
        if type == 1:
            self.report_stack_con.setCurrentIndex(0)
        elif type == 2:
            self.__load_examination_page_data()
            self.report__mark_export_btn.clicked.connect(self.__examination_detail)
            self.report_stack_con.setCurrentIndex(1)
        else:
            self.report_stack_con.setCurrentIndex(-1)
            

            
            
    def get_selected_items(self):
        selected_items = [
            self.report_columns.item(i).text()
            for i in range(self.report_columns.count())
            if self.report_columns.item(i).checkState()
        ]
        
        return selected_items
        
    def __load_file_types(self, file_type_obj : object):
        file_type_obj.setCurrentIndex(-1)
        file_type_obj.clear()
        if self.file_types:
            for title,id in self.file_types:
                file_type_obj.addItem( str(title), id)
    
    def __student_detail(self):
        class_id = self.report_class.currentData()
        section_id =  self.report_section.currentData()
        selected_columns = self.get_selected_items()
       
        file_type_id =  self.report_file_type.currentData()
        


        if not ( class_id and section_id and selected_columns and file_type_id):
            QMessageBox.warning(self,"Warning","Some Fields Missing , Please Select")
            return 0
        # print("selected columns = ",selected_columns)
        
        if not  ( len(selected_columns) >= 1 ):
            QMessageBox.warning(self,"Warning"," Please Select One or More Fields")
            return 0
        
        self.export_student_all_data(class_id, section_id, selected_columns)

    def export_student_all_data(self, class_id : int ,section_id : int, selected_columns : list):
        self.report_progress.setVisible(True)

        student_data = StudentDetails.get_all_by_class_and_section( class_id, section_id)

        if not (student_data and len(student_data) >= 1):
            QMessageBox.critical(self,"Error","No Student Data Found for this Class and Section")
        
        print("student data = ",student_data)
        sanitized_student_data = []
        self.report_progress.setValue(0)
        total_records = len(student_data)
        current_record = 1
        
        for data in student_data:
            item=data

            data = {
                "Id" : (str(item.id)),
                "Register No" : (str(item.register_no)),
                "Name" : (str(item.name)),
                "Date of Birth" : (str(item.dob) if item.dob else 'N/A'),
                "Email Id" : (str(item.email) if item.email else 'N/A'),
                "Address" : (str(item.personal_details.address) if item.personal_details and item.personal_details.address else 'N/A'),
                "Contact No" : (str(item.personal_details.contact_no) if item.personal_details and item.personal_details.contact_no else 'N/A'),
                "Ration Card No" : (str(item.personal_details.ration_card_no) if item.personal_details and item.personal_details.ration_card_no else 'N/A'),
                "Community" : (str(item.personal_details.community) if item.personal_details and item.personal_details.community else 'N/A'),
                "Adharr No" : (str(item.personal_details.adharr_no) if item.personal_details and item.personal_details.adharr_no else 'N/A'),
                "Account No" : (str(item.bank_details.account_no) if item.bank_details and item.bank_details.account_no else 'N/A'),
                "Bank Name" : (str(item.bank_details.bank_name) if item.bank_details and item.bank_details.bank_name else 'N/A'),
                "Branch Name" : (str(item.bank_details.branch_name) if item.bank_details and item.bank_details.branch_name else 'N/A'),
                "IFSC Code" : (str(item.bank_details.ifsc_code) if item.bank_details and item.bank_details.ifsc_code else 'N/A'),
                "MICR Code" : (str(item.bank_details.micr_code) if item.bank_details and item.bank_details.micr_code else 'N/A'),
                }
            # sanitizing with selected columns
            sanitized_student_data.append({key: value for key, value in data.items() if key in selected_columns})
            percentage = current_record  * 100 / total_records
            self.report_progress.setValue(int(percentage))
            current_record += 1
            
        self.sanitized_data_to_excel(sanitized_student_data)

    def sanitized_data_to_excel(self, records : list[dict]):
        if not records:
            QMessageBox.critical(self,"Error","Student Data Missing")
            return 0
        
        df = pd.DataFrame(records)
        
        file_path = QFileDialog.getSaveFileName(self, "Select Path To Save File", "", "Excel Files (*.xlsx)")
        
        if file_path and file_path[0]:
            df.to_excel( str(file_path[0]),index=False)
            QMessageBox.information(self,"Info",f"File Saved at {file_path[0]}")
        else:
            QMessageBox.critical(self,"Error","Operation Cancelled")
            
        self.report_progress.setVisible(False)

    def __examination_detail(self):
        class_id = int(self.report_mark_class_cb.currentData())
        section_id =  int(self.report_mark_class_cb.currentData())
        examination_id = 1
       
        file_type_id =  self.report_mark_file_type.currentData()

        if not ( class_id and section_id and examination_id and file_type_id):
            QMessageBox.warning(self,"Warning","Some Fields Missing , Please Select")
            return 0
    
        
        self.export_examination_all_data(class_id, section_id, examination_id)

    def export_examination_all_data(self, class_id : int ,section_id : int,examination_id : int):
        self.report_progress.setVisible(True)

        examination_data =  StudentDetails.get_marks_by_class_section_exam(class_id,section_id,1)
        # print("EXAMINATION DATA = ",examination_data)

        if not (examination_data and len(examination_data) >= 1):
            QMessageBox.critical(self,"Error","No Student Data Found for this Class and Section")
        
        sanitized_data = []
        sanitized_data.clear()
        
        for data in examination_data:
            _data = {
                "Register No" : data.get("register_no","N/  A"),
                "Name": data.get("student_name","N/A"),
                } 
            _data.update(
                dict(zip(data.get("subjects",[]),data.get("marks",[])))
            )
          
            sanitized_data.append(_data)
            data.clear()
            
        self.report_progress.setValue(0)
        # print("SANITIZED  DATA=",sanitized_data)
        self.sanitized_data_to_excel(sanitized_data)



    