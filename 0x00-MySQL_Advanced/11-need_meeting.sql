-- Need meeting

DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
AND (
    students.last_meeting IS NULL
    OR
    DATEDIFF(CURDATE(), students.last_meeting) > 30
);
