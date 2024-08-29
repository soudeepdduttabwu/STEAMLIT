SELECT 
    users.name,
    attendance.date,
    attendance.clockin_time AS ENTRY_TIME,
    attendance.clockout_time AS EXIT_TIME,
    TIMEDIFF(attendance.clockout_time, attendance.clockin_time) AS TOTAL_TIME_SPENT
FROM 
    git.attendance
JOIN 
    users ON users.id = attendance.user_id
WHERE 
    attendance.date BETWEEN '{start_date}' AND '{end_date}';