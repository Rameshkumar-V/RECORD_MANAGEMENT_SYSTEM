from frontend import FrontEnd
from master_page import MasterPage
from student_page import StudentPage
from mark_page import MarksPage
from report_page  import ReportPage
from setting_page import SettingPage
from school_page import SchoolPage

class BackEnd(
    FrontEnd,
    StudentPage,
    MasterPage,
    MarksPage,
    ReportPage,
    # SettingPage
    SchoolPage
    ):
    def __init__(self):
        FrontEnd.__init__(self)
        
        print("fronent end loaded")
        print(self.student_page_btn)
        MasterPage.__init__(self)
        print("master page loaded")
        MarksPage.__init__(self)
        print("student page load on")
        StudentPage.__init__(self)
        # print(self.student_page_btn)
        print("student page loaded")
        
        ReportPage.__init__(self)
        SchoolPage.__init__(self)
        # SettingPage.__init__(self)

        self.data = "Hello from the backend!"
        # MAIN PAGE ( parent )
        self.student_page_btn.clicked.connect(self.student_page)
        self.reports_page_btn.clicked.connect(self.reports_page)
        self.master_page_btn.clicked.connect(self.master_page)
        self.marks_page_btn.clicked.connect(self.marks_page)
        self.school_page_btn.clicked.connect(self.school_page)
        # self.setting_page_btn.clicked.connect(self.setting_page)
        """"
        PAGE - STUDENT PAGE
        info - Handling their stack containers and inside their widgets actions.
        """
        
      
        # STUDENT PAGE
        self.add_student_btn.clicked.connect(self.student_details_container)
        self.add_persoal_details.clicked.connect(self.student_personal_details)
        self.add_bank_details.clicked.connect(self.student_bank_details)
        # self.std_exam_container_btn.clicked.connect(self.student_examination_details)
        
        

        # STUDENT PAGE INSIDE
        self.std_add_btn.clicked.connect(self.save_student_details)
        
        """
        END OF STUDENT PAGE
        """
    
        
        
    
    # MAIN PAGE ( parent )
    def process_data(self, input_text):
        print("hellow world")
        return f"Processed: {input_text}"
    def student_page(self):
        self.main_stack.setCurrentIndex(0)
    def reports_page(self):
        self.main_stack.setCurrentIndex(1)
    def master_page(self):
        self.load_class_and_section(self.master_class_cb,self.master_section_cb)
        self.cb_event_listner_to_load_examination_name(self.master_class_cb,self.master_section_cb,self.master_exam_cb)
        self.master_class_cb.activated.connect(self.display_student_marks)
        self.master_section_cb.activated.connect(self.display_student_marks)
        self.master_exam_cb.activated.connect(self.display_student_marks)
        self.display_student_marks()
        # self.insert_row()
        self.main_stack.setCurrentIndex(2)
    def marks_page(self):
        self.load_class_and_section(self.mark_class_cb,self.mark_section_cb)
        # self.cb_event_listner_to_load_examination_name(self.mark_class_cb,self.mark_section_cb, self.mark_page_examination_cb)
        self.listen_class_and_section_for_register_no(self.mark_class_cb,self.mark_section_cb,self.mark_register_no_cb)
        self.main_stack.setCurrentIndex(3)
    def setting_page(self):
        
        self.main_stack.setCurrentIndex(4)
    def school_page(self):
        self.main_stack.setCurrentIndex(4)
        
        
        

    
    
