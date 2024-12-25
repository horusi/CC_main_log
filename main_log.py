import streamlit as st
import datetime
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject: str, body: str, to_email: str):
    from_email = "kwiley115907@outlook.com"
    password = "Abc123321cbA"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls() 
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

class EquipmentMaintenanceLog:
    def __init__(self):
        self.down_for_maintenance = {}
        self.need_inspection = {}
        self.quarterly_tune_ups = {}
        self.equipment_list = [
            'MS 170', 'MS 180c', 'MS 250', 'MS 290', 'MS 291', 
            'MS 362c', 'MS 500i', 'CS 400', 'CS 490', 'CS 2511T', 
            'CS 271T', 'CS 303T', 'TORO 25611HD', 'TORO 25615HD', 
            'VERMEER 252c', 'HT135 - pp', 'F450', 'F550'
        ]
        self.operator_list = ['RW', 'MV', 'MH', 'KW']

    def get_equipment_list(self):
        return self.equipment_list

    def get_operators_list(self):
        return self.operator_list

    def add_new_equipment(self, equipment_id: str):
        if equipment_id not in self.equipment_list:
            self.equipment_list.append(equipment_id)
            return True
        return False

    def add_new_operators(self, operators_id: str):
        if operators_id not in self.operator_list:
            self.operator_list.append(operators_id)
            return True
        return False

    def save_to_file(self, file_path: str, data: str):
        print("save_to_file called with data:", data)
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory {directory} created.")
            
        with open(file_path, 'a') as file:
            file.write(data + '/n')
            file.write("Down for Maintenance:\n")
            file.write(str(self.down_for_maintenance) + "\n")
            file.write("Need Inspection:\n")
            file.write(str(self.need_inspection) + "\n")
            file.write("Quarterly Tune Ups:\n")
            file.write(str(self.quarterly_tune_ups) + "\n")
            file.write("Equipment List:\n")
            file.write(str(self.equipment_list) + "\n")
        print("Data saved successfully!")
    
    def add_log(self, log_type: str, equipment: str, operator: str, description: str): 
        if log_type == 'maintenance': 
            self.down_for_maintenance[equipment] = {'operator': operator, 'description': description} 
        elif log_type == 'inspection': 
            self.need_inspection[equipment] = {'operator': operator, 'description': description} 
        elif log_type == 'tuneup': 
            self.quarterly_tune_ups[equipment] = {'operator': operator, 'description': description} 
        
        log_entry = f"{log_type.capitalize()} Log:\nEquipment: {equipment}\nOperator: {operator}\nDescription: {description}\n"
        
        self.save_to_file('logs/maintenance_logs.txt', log_entry) 
    
    # Send email notification 
        subject = f"New {log_type.capitalize()} Log Submitted" 
        body = f"Equipment: {equipment}\nOperator: {operator}\nDescription: {description}" 
        send_email(subject, body, "kwiley115907@outlook.com") 
    
    
    # Example usage 
maintenance_log = EquipmentMaintenanceLog()
        
            
def main():
    st.title("Equipment Maintenance Log")
    maintenance_log = EquipmentMaintenanceLog()

    # Equipment Down for Maintenance
    st.subheader("Equipment Down for Maintenance")
    with st.form(key="down_form", clear_on_submit=True):
        equipment_options = maintenance_log.get_equipment_list() + ["Other: Not Shown"]
        operator_options = maintenance_log.get_operators_list() + ["Other: Not Shown"]

        down_equipment_var = st.selectbox("Equipment", equipment_options)
        down_other_equipment_var = st.text_input("Specify Other Equipment") if down_equipment_var == "Other: Not Shown" else ""
        down_operator_var = st.selectbox("Operator Initials", operator_options)
        down_other_operator_var = st.text_input("Specify Other Operator") if down_operator_var == "Other: Not Shown" else ""
        down_description_input = st.text_area("Description of Work Needed")

        submitted = st.form_submit_button("Add Equipment Down")
        if submitted:
            equipment = down_other_equipment_var if down_equipment_var == "Other: Not Shown" else down_equipment_var
            operator = down_other_operator_var if down_operator_var == "Other: Not Shown" else down_operator_var
            description = down_description_input

            if equipment and operator and description:
                st.success(f"Equipment down added: {equipment} by {operator} with description: {description}")
                maintenance_log.add_log('maintenance', equipment, operator, description)
            else:
                st.error("Please complete all fields")

    st.markdown("---")
    
    # Equipment Needing Inspection
    st.subheader("Equipment Needing Inspection")
    with st.form(key="inspection_form", clear_on_submit=True):
        inspection_equipment_var = st.selectbox("Equipment", equipment_options, key="inspection_equipment")
        inspection_other_equipment_var = st.text_input("Specify Other Equipment", key="inspection_other_equipment") if inspection_equipment_var == "Other: Not Shown" else ""
        inspection_operator_var = st.selectbox("Operator Initials", operator_options, key="inspection_operator")
        inspection_other_operator_var = st.text_input("Specify Other Operator", key="inspection_other_operator") if inspection_operator_var == "Other: Not Shown" else ""
        inspection_description_input = st.text_area("Description of Inspection Needed", key="inspection_description")

        submitted = st.form_submit_button("Add Inspection")
        if submitted:
            equipment = inspection_other_equipment_var if inspection_equipment_var == "Other: Not Shown" else inspection_equipment_var
            operator = inspection_other_operator_var if inspection_operator_var == "Other: Not Shown" else inspection_operator_var
            description = inspection_description_input

            if equipment and operator and description:
                st.success(f"Inspection added: {equipment} by {operator} with description: {description}")
                maintenance_log.add_log('Equipment Needing Inspection', equipment, operator, description)
            else:
                st.error("Please complete all fields")
    
    st.markdown("---")
    
    # Quarterly Tune-Ups
    st.subheader("Quarterly Tune-Ups")
    with st.form(key="tuneup_form", clear_on_submit=True):
        tuneup_equipment_var = st.selectbox("Equipment", equipment_options, key="tuneup_equipment")
        tuneup_other_equipment_var = st.text_input("Specify Other Equipment", key="tuneup_other_equipment") if tuneup_equipment_var == "Other: Not Shown" else ""
        tuneup_operator_var = st.selectbox("Operator Initials", operator_options, key="tuneup_operator")
        tuneup_other_operator_var = st.text_input("Specify Other Operator", key="tuneup_other_operator") if tuneup_operator_var == "Other: Not Shown" else ""
        tuneup_date_var = st.text_input("Scheduled Date (DD-MM-YYYY)", key="tuneup_date")

        submitted = st.form_submit_button("Schedule Tune-Up")
        if submitted:
            equipment = tuneup_other_equipment_var if tuneup_equipment_var == "Other: Not Shown" else tuneup_equipment_var
            operator = tuneup_other_operator_var if tuneup_operator_var == "Other: Not Shown" else tuneup_operator_var
            date_str = tuneup_date_var

            try:
                scheduled_date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                st.error("Invalid date format. Use DD-MM-YYYY")
                return

            if equipment and operator:
                st.success(f"Tune-Up scheduled for {equipment} on {scheduled_date} by {operator}")
                maintenance_log.add_log('Quarterly Tune-Up Scheduled', equipment, operator, scheduled_date)
            else:
                st.error("Please select equipment and operator initials")

if __name__ == "__main__":
    main()
