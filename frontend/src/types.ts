export interface Employee {
  name: string;
  employee_no: string;
  department: string;
  position_title: string;
  date_hired: string;
  last_day: string;
  um: string;
  um_late: boolean;
  third_party: string;
  third_party_late: boolean;
  email: string;
  email_late: boolean;
  windows: string;
  windows_late: boolean;
  date_hr_emailed: string;
  processed_date_time?: string | null;
  cost_center?: string;
  rank?: string;
  remarks: string;
}