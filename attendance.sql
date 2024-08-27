SELECT attendance.user_id,
    users.name AS Name ,
    attendance.clockin_time AS Entry_time ,
    attendance.clockin_address AS Entry_Address ,
    attendance.clockout_time AS Exit_time,
    attendance.clockout_address AS Exit_Address,
    attendance.date
FROM 
    git.attendance
JOIN 
    users 
ON 
    users.id = attendance.user_id
WHERE 
    attendance.date BETWEEN '{start_date}' AND '{end_date}';

