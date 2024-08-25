-- Average

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score DECIMAL(10,2);
    DECLARE total_count INT;

    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    SELECT COUNT(*) INTO total_count
    FROM corrections
    WHERE corrections.user_id = user_id;

    SET @average_score = total_score / total_count;

    UPDATE users
    SET average_score = @average_score
    WHERE id = user_id;
END//
DELIMITER ;
