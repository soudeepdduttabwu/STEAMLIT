SELECT 
leave_reason.id as leave_id,
u1.name AS user_name,
DATE(leave_reason.created_at) AS Leave_mark_Date,
leave_reason.date1 AS start_date,
leave_reason.date2 AS end_date,
leave_reason.reason,
leave_reason.status AS leave_status
FROM 
    git.leave_reason
JOIN 
    users u1 ON u1.id = leave_reason.user_id
WHERE 
    DATE(leave_reason.created_at) BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59';