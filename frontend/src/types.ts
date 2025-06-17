export interface Employee {
  name: string;
  employee_no: string;
  department: string;
  position_title: string;
  date_hired: string;
  last_day: string;
  processed_date_time?: string | null;
  cost_center?: string;
  rank?: string;
}