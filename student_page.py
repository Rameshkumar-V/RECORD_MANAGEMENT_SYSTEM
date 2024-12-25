from database.models import *
from validator import Validator
from PyQt5.QtWidgets import  QMessageBox
class StudentPage:
    # PAGES
    def student_details_container(self):
        """
        STUDENT DETAILS
        """
        self.load_class_and_section( self.std_add_class_cb, self.std_add_section_cb)
        self.std_stack_con.setCurrentIndex(0)

    def student_personal_details(self):
        """
        PERSONAL DETAILS
        """
        self.load_class_and_section( self.std_pd_class_cb, self.std_pd_section_cb)
        self.listen_class_and_section_for_register_no( self.std_pd_class_cb,self.std_pd_section_cb,self.std_pd_register_no_e)
        self.std_stack_con.setCurrentIndex(1)
        self.std_pd_add_btn.clicked.connect(self.save_personal_details)
        self.std_pd_register_no_e.activated.connect(self.std_pd_register_no_listener)

    def student_bank_details(self):
        """
        BANK DETAILS
        """
        self.load_class_and_section(self.std_bank_class_cb,self.std_bank_section_cb)
        self.listen_class_and_section_for_register_no( self.std_bank_class_cb, self.std_bank_section_cb, self.std_bank_register_no_e)
        self.std_stack_con.setCurrentIndex(2)
        self.std_bank_add_btn.clicked.connect(self.save_bank_details)
        self.std_bank_register_no_e.activated.connect(self.std_bank_register_no_listener)
    
    # LOADING CLASS AND SECTION FOR ALL UI
    def load_class_and_section(self, class_obj, section_obj):
        """
        Load Class and Section Items with their objects.
        """
       
        class_data = Class.get_all()
        section_data = Section.get_all()
        
        class_obj.clear()
        section_obj.clear()
        
        if class_data:
            for class_item in class_data:
                class_obj.addItem(class_item.name, class_item.id)

        if section_data:
            for section_item in section_data:
                section_obj.addItem(section_item.name, section_item.id)

            
        section_obj.setCurrentIndex(-1)
        class_obj.setCurrentIndex(-1)
  
    # LOADING REGNO WITH CLASS AND SECTION FOR ALL UI
    def listen_class_and_section_for_register_no(self, class_obj, section_obj, register_no_obj):
        """
        Load Regiter No with class and section objects.
        When Class or Secton Activated then data Can be loaded.
        """
        def load_data():
            class_obj_data = class_obj.currentData()
            section_obj_data = section_obj.currentData()
      
            if (class_obj_data != None and class_obj_data >= 0 ) and ( section_obj_data != None and section_obj_data >= 0):
                register_no_data = StudentDetails.get_by_class_and_section( class_obj_data, section_obj_data)

                if  register_no_data:
                    register_no_obj.clear()
                    register_no_obj.setEnabled(True)
                    for no,id in register_no_data:
                        register_no_obj.addItem(str(no), id)
                
                else:
                    register_no_obj.clear()
            else:
                pass
            
        class_obj.activated.connect(load_data)
        section_obj.activated.connect(load_data)
        
    # STUDENT DETAILS
    def save_student_details(self):
            """
            Saving Student Details on Database.
            """
            # #print("yeah well")
            is_valid_form = self.validate_student_details()
            if not is_valid_form:
                return 0 
            register_no = self.student_reg_no.text()
            name = self.student_name_e.text()
            dob = self.student_dob_e.date().toPyDate()
            email = self.student_email_e.text()
            cid=self.std_add_class_cb.currentData()
            sid=self.std_add_section_cb.currentData()
            
            if ( register_no and name and dob and email and  cid >= 0 and sid >= 0):
                result = StudentDetails.add(
                                            register_no=register_no,
                                            name=name,
                                            dob=dob,
                                            email=email, 
                                            class_id=cid, 
                                            section_id=sid )
                if result.get("status",None) == "success":
                    QMessageBox.information(self, "Info", "Student Record Saved")
                else:
                    QMessageBox.critical(self, "Warning",str(result.get("error","Invalid")) )
            else:
                QMessageBox.warning(self, "Warning", "Some Field Data Missing !")
                
    # PERSONAL DETAILS
    def save_personal_details(self):
        """
        Saving Student's Personal details on Database.
        """
        is_valid_form = self.validate_personal_details()
        if not is_valid_form:
            return 0 
        register_no : int = self.std_pd_register_no_e.currentData()
        adharr_no : int = self.std_pd_add_adhaar_no.text()
        address : str = self.std_pd_address_no.toPlainText()
        contact_no : int = self.std_pd_contact_no.text()
        ration_card_no : int = self.std_pd_ration_card_no.text()
        community : str = self.std_pd_community_no.text()

        if not (register_no and adharr_no and address and contact_no and ration_card_no and community):
            QMessageBox.warning(self,"Warning","Invalid Data, Some Fields Missing")
            return 0
        

        result = StudentPersonalDetails.add(
            student_id = register_no,
            adharr_no = adharr_no,
            address = address,
            contact_no = contact_no,
            ration_card_no = ration_card_no,
            community = community
        )
        if result.get("status")=="success":
            QMessageBox.information(self,"Info","Record Saved")
            register_no.setCurrentIndex(-1)
            adharr_no.setText('')
            address.setText('')
            contact_no.setText('')
            ration_card_no.setText('')
            community.setText('')

        else:
            QMessageBox.critical(self,"Error","Invalid Data")
    def std_pd_register_no_listener(self):
        """"
        Register no Changed or Activated to Show Add or Update Button
        if data
        """
        add_btn_obj = self.std_pd_add_btn
        update_btn_obj = self.std_pd_update_btn
        register_no : int = self.std_pd_register_no_e.currentData()
        
        student_data = StudentDetails.get_by_id(int(register_no))
        
        if student_data and student_data.personal_details:

            self.std_pd_add_adhaar_no.setText(str(student_data.personal_details.adharr_no))
            self.std_pd_address_no.setText(str(student_data.personal_details.address))
            self.std_pd_contact_no.setText(str(student_data.personal_details.contact_no))
            self.std_pd_ration_card_no.setText(str(student_data.personal_details.ration_card_no))
            self.std_pd_community_no.setText(str(student_data.personal_details.community))

            add_btn_obj.setVisible(False)
            update_btn_obj.setVisible(True)

        else:
            self.std_pd_add_adhaar_no.setText('')
            self.std_pd_address_no.setText('')
            self.std_pd_contact_no.setText('')
            self.std_pd_ration_card_no.setText('')
            self.std_pd_community_no.setText('')

            add_btn_obj.setVisible(True)
            update_btn_obj.setVisible(False)

    # BANK DETAILS
    def save_bank_details(self):
        """
        Saving Bank Details on Database.
        """
        ##print("SAVE BANK DETAILS CALLED")
        is_valid_form = self.validate_bank_details()
        if not is_valid_form:
            return 0 
      
            
        register_no : int = self.std_bank_register_no_e.currentData()
        account_no : int = self.std_bank_account_no.text()
        bank_name : str = self.std_bank_name.text()
        branch_name : str = self.std_mark_branch_name.text()
        ifsc_code : str = self.std_mark_ifsc_code.text()
        micr_code : str = self.std_mark_micr_code.text()

        if not (register_no and account_no and bank_name and branch_name and ifsc_code and micr_code):
            QMessageBox.warning(self,"Warning","Invalid Data, Some Fields Missing")
            return 0

        result = StudentBankDetails.add(
            student_id = register_no,
            account_no = account_no,
            bank_name = bank_name,
            branch_name = branch_name,
            ifsc_code = ifsc_code,
            micr_code = micr_code
        )
        if result.get("status")=="success":
            self.std_bank_account_no.setText('')
            self.std_bank_name.setText('')
            self.std_mark_branch_name.setText('')
            self.std_mark_ifsc_code.setText('')
            self.std_mark_micr_code.setText('')
            QMessageBox.information(self,"Info","Record Saved")
        else:
            QMessageBox.critical(self,"Error","Invalid Data")
    def std_bank_register_no_listener(self):
        """"
        Register no Changed or Activated to Show Add or Update Button
        if data
        """
        add_btn_obj = self.std_bank_add_btn
        update_btn_obj = self.std_bank_update_btn
        register_no : int = self.std_bank_register_no_e.currentData()
        

        student_data = StudentDetails.get_by_id(int(register_no))

        if student_data and student_data.bank_details:

            self.std_bank_account_no.setText(str(student_data.bank_details.account_no))
            self.std_bank_name.setText(str(student_data.bank_details.bank_name))
            self.std_mark_branch_name.setText(str(student_data.bank_details.branch_name))
            self.std_mark_ifsc_code.setText(str(student_data.bank_details.ifsc_code))
            self.std_mark_micr_code.setText(str(student_data.bank_details.micr_code))

            add_btn_obj.setVisible(False)
            update_btn_obj.setVisible(True)
        else:
            self.std_bank_account_no.setText('')
            self.std_bank_name.setText('')
            self.std_mark_branch_name.setText('')
            self.std_mark_ifsc_code.setText('')
            self.std_mark_micr_code.setText('')

            add_btn_obj.setVisible(True)
            update_btn_obj.setVisible(False)

    # VALIDATION
    def validate_student_details(self) -> bool :
        register_no = self.student_reg_no.text()
        name = self.student_name_e.text()
        dob = self.student_dob_e.date().toPyDate()
        email = self.student_email_e.text()
        
        is_register_no =Validator.validate_register_no(register_no)
        is_name = Validator.validate_name(name)
        is_dob = Validator.validate_dob(dob)
        is_email = Validator.validate_mail_id(email)
        
        is_valid = True
        
        if not is_register_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Register No !")
        if not is_name:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Name!")
        if not is_dob:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Date of Birth !")
        if not is_email:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Mail Id !")
            
        return is_valid
    def validate_personal_details(self) -> bool :
        register_no : int = self.std_pd_register_no_e.currentText()
        adhaar_no : int = self.std_pd_add_adhaar_no.text()
        address : str = self.std_pd_address_no.toPlainText()
        contact_no : int = self.std_pd_contact_no.text()
        ration_card_no : int = self.std_pd_ration_card_no.text()
        community : str = self.std_pd_community_no.text()
        
        is_register_no =Validator.validate_register_no(str(register_no))
        is_adhaar_no = Validator.validate_aadhar_no(str(adhaar_no))
        is_address = Validator.validate_address(address)
        is_contact_no = Validator.validate_contact_no(str(contact_no))
        is_ration_no = Validator.validate_ration_card_no(str(ration_card_no))
        is_community = Validator.validate_community(community)
        
        is_valid = True
        if not is_register_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Register No !")
        if not is_adhaar_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Adhaar no !")
        if not is_address:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Address !")
        if not is_contact_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Contact No !")
        if not is_ration_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Ration Card No !")
        if not is_community:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Community !")
        
        return is_valid
    def validate_bank_details(self) -> bool :
        register_no : int = self.std_bank_register_no_e.currentText()
        account_no : int = self.std_bank_account_no.text()
        bank_name : str = self.std_bank_name.text()
        branch_name : str = self.std_mark_branch_name.text()
        ifsc_code : str = self.std_mark_ifsc_code.text()
        micr_code : str = self.std_mark_micr_code.text()
        
        is_register_no : bool = Validator.validate_register_no(register_no)
        is_account_no : bool = Validator.validate_account_no(account_no)
        is_bank_name : bool = Validator.validate_bank_name(bank_name)
        is_ifsc_code : bool = Validator.validate_ifsc_code(ifsc_code)
        is_micr_code : bool =Validator.validate_micr_code(micr_code)
        
        is_valid = True
        
        if not is_register_no:
            is_valid = False
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Register No !")
        if not is_account_no:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Account No !") 
        if not is_bank_name:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  Bank Name !")
        if not is_ifsc_code:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  IFSC code !")
        if not is_micr_code:
            is_valid = False
            QMessageBox.warning(self, "Warning", "Please Provide valid  MICR code !")
        
        return is_valid
