from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import  QPushButton,QMessageBox
from database.models import *


class MasterPage:
    def __init__(self):
        
        self.model = QStandardItemModel()
        self.student_detail_headers = ["ID", "Register No ", "Name","DOB","Email Id","Address"]
        self.personal_detail_headers = ["ID","Contact No","Ration Card No","Community","Adharr No",]
        self.bank_detail_headers = ["ID","Bank Account No","Bank Name","Branch Name","IFSC code","MICR code"]
        self.combined_headers = self.student_detail_headers + self.personal_detail_headers + self.bank_detail_headers

        self.master_header = list(dict.fromkeys(self.combined_headers))+["Delete"]
        self.student_marks_master_header = [
                "Register No",
                "Name",
            ]
        self.master_type_data = dict({
            "SHOW STUDENT":1,
            "SHOW MARKS" : 2
        })
        self.load_master_type_cb()
        
        # self.master_show_btn.clicked.connect(self.student_records_show)
        self.master_type_cb.activated.connect(self.master_diplay_handler)
    def load_master_type_cb(self):
        for name,id in self.master_type_data.items():
            self.master_type_cb.addItem(str(name),int(id))
            
    def master_diplay_handler(self):
        """
        Master Page Table Diplay Handler
        """
        type_id : int = int(self.master_type_cb.currentData())
        print(type_id)
        if not type_id:
            return 0
        
        if type_id == 1:
            self.display_student_records()
        elif type_id == 2:
            self.display_student_marks()
        else:
            return 0

        
        
        
        
    def delete_row(self, student_id : int):
        print("hello student = ",student_id)

    def display_student_records(self):
        
        section_id = self.master_section_cb.currentData()
        class_id = self.master_class_cb.currentData()

        if not (section_id and class_id):
            QMessageBox.warning(self,"Warning","Please Select Class and Section ")
            return 0
        
        student_data = StudentDetails.get_all_by_class_and_section(class_id,section_id)
        if not student_data:
            QMessageBox.warning(self,"Warning","No Records Currently Available")
            return 0
            
        """Insert a new row into the table with default values."""
        # Define default data for the new row
        self.master_student_table.setModel(self.model)
        default_id = str(self.model.rowCount() + 1)  # Auto-increment ID
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.master_header)
        
       
        # Add the row to the model
        for  item in student_data:
           
           # Resize to content max size
            self.master_student_table.resizeRowsToContents()
            self.master_student_table.resizeColumnsToContents()
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda: self.delete_row(item.id))
        
            row_items =([
                QStandardItem(str(item.id)),
                QStandardItem(str(item.register_no)),
                QStandardItem(str(item.name)),
                QStandardItem(str(item.dob) if item.dob else 'N/A'),
                QStandardItem(str(item.email) if item.email else 'N/A'),
                QStandardItem(str(item.personal_details.address) if item.personal_details and item.personal_details.address else 'N/A'),
                QStandardItem(str(item.personal_details.contact_no) if item.personal_details and item.personal_details.contact_no else 'N/A'),
                QStandardItem(str(item.personal_details.ration_card_no) if item.personal_details and item.personal_details.ration_card_no else 'N/A'),
                QStandardItem(str(item.personal_details.community) if item.personal_details and item.personal_details.community else 'N/A'),
                QStandardItem(str(item.personal_details.adharr_no) if item.personal_details and item.personal_details.adharr_no else 'N/A'),
                QStandardItem(str(item.bank_details.account_no) if item.bank_details and item.bank_details.account_no else 'N/A'),
                QStandardItem(str(item.bank_details.bank_name) if item.bank_details and item.bank_details.bank_name else 'N/A'),
                QStandardItem(str(item.bank_details.branch_name) if item.bank_details and item.bank_details.branch_name else 'N/A'),
                QStandardItem(str(item.bank_details.ifsc_code) if item.bank_details and item.bank_details.ifsc_code else 'N/A'),
                QStandardItem(str(item.bank_details.micr_code) if item.bank_details and item.bank_details.micr_code else 'N/A'),
            ])
            row = self.model.rowCount()
            self.model.appendRow(row_items)
    
            # Create and set delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, student_id=item.id: self.delete_row(student_id))
            self.master_student_table.setIndexWidget(self.model.index(row, len(row_items)), delete_button)

            # self.master_student_table.setColumnHidden(0, True)  # Show the "ID" column
            self.master_student_table.verticalHeader().setVisible(False)
    def display_student_marks(self):
        self.master_student_table.setModel(self.model)
        self.model.clear()
        print("display student marks")
        
        section_id = self.master_section_cb.currentData()
        class_id = self.master_class_cb.currentData()
        examination_id = self.master_exam_cb.currentData()
        

        if not (section_id and class_id and examination_id):
            # QMessageBox.warning(self,"Warning","Please Select Class and Section ")
            return 0
        
        student_mark_data = StudentDetails.get_marks_by_class_section_exam(class_id,section_id,examination_id)
        if not student_mark_data:
            self.model.clear()
            QMessageBox.warning(self,"Warning","No Records Currently Available")
            return 0
        
        
        subject = student_mark_data[0].get("subjects")
        marks_header : list = self.student_marks_master_header + subject
        self.model.setHorizontalHeaderLabels(marks_header)
        # return 0
        
        
        for  item in student_mark_data:
           
           # Resize to content max size
            self.master_student_table.resizeRowsToContents()
            self.master_student_table.resizeColumnsToContents()
            
            row_items =([
                QStandardItem(str(item.get("register_no","NIL"))),
                QStandardItem(str(item.get("student_name","NIL"))),
                
            ]+ [QStandardItem(str(mark))  for mark in item.get("marks",[])])
            self.model.appendRow(row_items)
            
                
        
            
        
