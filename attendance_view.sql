SELECT 
    attendance.date, 
    attendance.user_id, 
    users.name AS Name, 
    attendance.clockin_time AS Entry_time, 
    attendance.clockin_address AS Entry_Address, 
    attendance.clockout_time AS Exit_time, 
    attendance.clockout_address AS Exit_Address, 
    attendance.absent_time as Absent_time, 
    attendance.absent_address as Absent_address, 
    attendance.reason as Absent_reason 
FROM 
    git.attendance 
JOIN 
    users 
ON 
    users.id = attendance.user_id 
WHERE 
    attendance.date BETWEEN '{start_date}' AND '{end_date}' 
AND 
    attendance.user_id = {user_id};
