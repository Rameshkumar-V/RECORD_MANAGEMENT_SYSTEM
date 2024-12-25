import re
from datetime import datetime,date

class Validator:
    @staticmethod
    def validate_register_no(register_no: str) -> bool:
        register_no = str(register_no)
        """
        Validate Register Number.
        Criteria: Alphanumeric and length between 5 and 15.
        """
        if not register_no:
            return False
        return bool(re.match(r"^\d{5,15}$", register_no))

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate Name.
        Criteria: Only alphabets and spaces, length between 2 and 50.
        """
        if not name:
            return False
        return bool(re.match(r"^[a-zA-Z\s]{2,50}$", name.strip()))

    @staticmethod
    def validate_dob(dob: str) -> bool:
        """
        Validates the date of birth format (YYYY-MM-DD).

        :param dob: Date of birth as a string or a date object.
        :return: Boolean indicating if the DOB is valid.
        """
        # If `dob` is a `datetime.date`, convert it to a string
        if isinstance(dob, date):  # Handles both `date` and `datetime.date`
            dob = dob.strftime("%Y-%m-%d")

        try:
            parsed_date = datetime.strptime(dob, "%Y-%m-%d")
            return True  # DOB is valid
        except ValueError:
            return False  # Invalid format or date

    @staticmethod
    def validate_mail_id(mail_id: str) -> bool:
        """
        Validate Email ID.
        Criteria: Must follow standard email format.
        """
        if not mail_id:
            return False
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", mail_id))

    @staticmethod
    def validate_address(address: str) -> bool:
        """
        Validate Address.
        Criteria: Non-empty string with at least 10 characters and up to 255 characters.
        """
        if not address:
            return False
        return 10 <= len(address.strip()) <= 255

    @staticmethod
    def validate_contact_no(contact_no: str) -> bool:
        """
        Validate Contact Number.
        Criteria: Exactly 10 digits.
        """
        if not contact_no:
            return False
        return bool(re.match(r"^\d{10}$", contact_no))

    @staticmethod
    def validate_ration_card_no(ration_card_no: str) -> bool:
        """
        Validate Ration Card Number.
        Criteria: Alphanumeric and length between 8 and 12.
        """
        if not ration_card_no:
            return False
        return bool(re.match(r"^[a-zA-Z0-9]{8,12}$", ration_card_no))

    @staticmethod
    def validate_community(community: str) -> bool:
        """
        Validate Community String.
        Criteria: Alphabetical string (case insensitive), length between 3 and 30.
        """
        if not community:
            return False
        return bool(re.match(r"^[a-zA-Z\s]{3,30}$", community.strip()))

    @staticmethod
    def validate_aadhar_no(aadhar_no: str) -> bool:
        """
        Validate Aadhar Number.
        Criteria: Exactly 12 digits.
        """
        if not aadhar_no:
            return False
        return bool(re.match(r"^\d{12}$", aadhar_no))


    # Bank Field Validators
    @staticmethod
    def validate_account_no(account_no: str) -> bool:
        """
        Validate Bank Account Number.
        Criteria: Numeric string, length between 9 and 18.
        """
        if not account_no:
            return False
        return bool(re.match(r"^\d{9,18}$", account_no))

    @staticmethod
    def validate_bank_name(bank_name: str) -> bool:
        """
        Validate Bank Name.
        Criteria: Alphabetical string (case insensitive), length between 3 and 50.
        """
        if not bank_name:
            return False
        return bool(re.match(r"^[a-zA-Z\s]{3,50}$", bank_name.strip()))

    @staticmethod
    def validate_branch_name(branch_name: str) -> bool:
        """
        Validate Branch Name.
        Criteria: Alphabetical string (case insensitive), length between 3 and 50.
        """
        if not branch_name:
            return False
        return bool(re.match(r"^[a-zA-Z\s]{3,50}$", branch_name.strip()))

    @staticmethod
    def validate_ifsc_code(ifsc_code: str) -> bool:
        """
        Validate IFSC Code.
        Criteria: 4 uppercase letters followed by 0 and 6 digits.
        Example: ABCD0123456
        """
        if not ifsc_code:
            return False
        return bool(re.match(r"^[A-Z]{4}0\d{6}$", ifsc_code))

    @staticmethod
    def validate_micr_code(micr_code: str) -> bool:
        """
        Validate MICR Code.
        Criteria: Exactly 9 digits.
        """
        if not micr_code:
            return False
        return bool(re.match(r"^\d{9}$", micr_code))
