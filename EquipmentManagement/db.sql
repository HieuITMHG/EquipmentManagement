DROP DATABASE IF EXISTS defaultdb;
CREATE DATABASE defaultdb;
USE defaultdb;

/* CREATE TABLE SCRIPT */
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) NOT NULL
);

CREATE TABLE privilege (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    privilege_name VARCHAR(100) NOT NULL
);

CREATE TABLE role_privilege (
    privilege_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (privilege_id, role_id),
    FOREIGN KEY (privilege_id) REFERENCES privilege(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE account (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(500) NOT NULL,
    role_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE person (
    id VARCHAR(20) PRIMARY KEY,
    cccd CHAR(12) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender BOOLEAN NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone CHAR(10) NOT NULL,
    address VARCHAR(255) NOT NULL,
    img_url VARCHAR(255) NOT NULL,
    account_id INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE TABLE department (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE class (
    id CHAR(20) PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL UNIQUE,
    academic_year CHAR(9) NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE room (
    id CHAR(5) PRIMARY KEY,
    floor_number INTEGER NOT NULL,
    section CHAR(1) NOT NULL,
    max_people INTEGER NOT NULL
);

CREATE TABLE student (
    id VARCHAR(20) PRIMARY KEY,
    class_id CHAR(20) NOT NULL,
    is_studing BOOLEAN NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(id),
    FOREIGN KEY (id) REFERENCES person(id)
);

CREATE TABLE staff (
    id VARCHAR(20) PRIMARY KEY,
    is_working BOOLEAN NOT NULL,
    FOREIGN KEY (id) REFERENCES person(id)
);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    equipment_name VARCHAR(50) NOT NULL,
    status ENUM('AVAILABLE', 'UNDERREPAIR', 'BORROWED', 'BROKEN', 'LIQUIDATED') NOT NULL,
    equipment_type ENUM('MOBILE', 'FIXED', 'SHARED') NOT NULL,
    room_id CHAR(5),
    FOREIGN KEY (room_id) REFERENCES room(id)
);

CREATE TABLE borrow_request (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    student_id CHAR(10) NOT NULL,
    staff_id CHAR(10),
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','RETURNED') NOT NULL DEFAULT 'PENDING',
    borrowing_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expect_returning_time DATETIME NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE borrow_item (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    actual_returning_time DATETIME,
    borrow_request_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    FOREIGN KEY (borrow_request_id) REFERENCES borrow_request(id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

CREATE TABLE penalty_form (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    form_name VARCHAR(100) NOT NULL,
    price DOUBLE
);

CREATE TABLE penalty_ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    staff_id CHAR(10) NOT NULL,
    student_id CHAR(10) NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','RETURNED') NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    FOREIGN KEY (student_id) REFERENCES student(id)
);

CREATE TABLE violation (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    violation_content VARCHAR(100) NOT NULL,
    penalty_form_id INTEGER NOT NULL,
    FOREIGN KEY (penalty_form_id) REFERENCES penalty_form(id)
);

CREATE TABLE detail_penalty_ticket (
    violation_id INTEGER NOT NULL,
    penalty_ticket_id INTEGER NOT NULL,
    PRIMARY KEY (violation_id, penalty_ticket_id),
    FOREIGN KEY (violation_id) REFERENCES violation(id),
    FOREIGN KEY (penalty_ticket_id) REFERENCES penalty_ticket(id)
);

CREATE TABLE repair_ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','RETURNED') NOT NULL,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE detail_repair_ticket (
    repair_ticket_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    price INTEGER,
    PRIMARY KEY (repair_ticket_id, equipment_id),
    FOREIGN KEY (repair_ticket_id) REFERENCES repair_ticket(id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

CREATE TABLE liquidation_slip (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    liquidation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE detail_liquidation_slip (
    liquidation_slip_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    PRIMARY KEY (liquidation_slip_id, equipment_id),
    FOREIGN KEY (liquidation_slip_id) REFERENCES liquidation_slip(id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

/* INSERT SAMPLE DATA */
-- Insert sample data for role
INSERT INTO role (role_name) VALUES 
('Manager'), 
('Student'), 
('Staff');

-- Insert sample data for privilege
INSERT INTO privilege (privilege_name) VALUES 
('Borrow Equipment'), 
('Manage Users'), 
('Manage Equipment');

-- Insert sample data for role_privilege
INSERT INTO role_privilege (privilege_id, role_id) VALUES 
(1, 2), -- Students can borrow equipment
(2, 1), -- Admins can manage users
(3, 3); -- Staff can manage equipment

-- Insert sample data for department
INSERT INTO department (department_name) VALUES 
('Computer Science'), 
('Electronics'), 
('Mechanical Engineering');

-- Insert sample data for class
INSERT INTO class (id, class_name, academic_year, department_id) VALUES 
('D22CQCN02-N', 'Công nghệ thông tin 2', '2022-2027', 1), 
('D22CQCN01-N', 'Công nghệ thông tin 1', '2022-2027', 2);

-- Insert sample data for room
INSERT INTO room (id, floor_number, section, max_people) VALUES 
('2B25', 2, 'B', 80), 
('2A16', 1, 'A', 100),
('2E21', 2, 'E', 50), 
('2E22', 2, 'E', 80);

-- Insert sample data for fixed equipment (each room has one speaker and one projector)
-- Insert fixed equipment
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
('Speaker', 'AVAILABLE', 'FIXED', '2B25'), 
('Speaker', 'AVAILABLE', 'FIXED', '2A16'), 
('Projector', 'AVAILABLE', 'FIXED', '2B25'), 
('Projector', 'AVAILABLE', 'FIXED', '2A16'), 
('Blackboard', 'AVAILABLE', 'FIXED', '2B25'), 
('Blackboard', 'AVAILABLE', 'FIXED', '2A16'), 
('Table', 'AVAILABLE', 'FIXED', '2B25'), 
('Table', 'AVAILABLE', 'FIXED', '2A16'), 
('Chair', 'AVAILABLE', 'FIXED', '2B25'), 
('Chair', 'AVAILABLE', 'FIXED', '2A16'), 
('Screen', 'AVAILABLE', 'FIXED', '2B25'), 
('Screen', 'AVAILABLE', 'FIXED', '2A16'), 
('Fan', 'AVAILABLE', 'FIXED', '2B25'), 
('Fan', 'AVAILABLE', 'FIXED', '2A16');

-- Insert mobile equipment
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
-- Room 2B25
('Microphone', 'AVAILABLE', 'MOBILE', '2B25'), 
('Microphone', 'AVAILABLE', 'MOBILE', '2B25'), 
('Key', 'AVAILABLE', 'MOBILE', '2B25'), 
('Key', 'AVAILABLE', 'MOBILE', '2B25'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2B25'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2B25'), 

-- Room 2A16
('Microphone', 'AVAILABLE', 'MOBILE', '2A16'), 
('Microphone', 'AVAILABLE', 'MOBILE', '2A16'), 
('Key', 'AVAILABLE', 'MOBILE', '2A16'), 
('Key', 'AVAILABLE', 'MOBILE', '2A16'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2A16'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2A16');

-- Insert shared equipment
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
('Microphone', 'AVAILABLE', 'SHARED', NULL), 
('Key', 'AVAILABLE', 'SHARED', NULL);

-- Insert special equipment in 2E21, 2E22
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
-- Room 2E21
('IoT Toolkit', 'AVAILABLE', 'FIXED', '2E21'), 
('Electronics Practice Kit', 'AVAILABLE', 'FIXED', '2E21'), 

-- Room 2E22
('IoT Toolkit', 'AVAILABLE', 'FIXED', '2E22'), 
('Electronics Practice Kit', 'AVAILABLE', 'FIXED', '2E22');


-- Chèn tài khoản cho sinh viên
INSERT INTO account (password, role_id, is_active) VALUES 
('student123', 2, TRUE),  -- Tài khoản cho 'N22DCCN127'
('student456', 2, TRUE);  -- Tài khoản cho 'N22DCCN078'

-- Chèn tài khoản cho nhân viên
INSERT INTO account (password, role_id, is_active) VALUES 
('staff123', 3, TRUE),  -- Tài khoản cho 'STF2001'
('staff456', 3, TRUE);  -- Tài khoản cho 'STF2002'

-- Chèn thông tin cá nhân cho sinh viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, img_url, account_id) VALUES 
('N22DCCN127', '123456789012', 'Hieu', 'Nguyen', TRUE, 'hieu127@example.com', '0987654321', 'Hanoi, Vietnam', 'hieu127.jpg', 1),
('N22DCCN078', '987654321012', 'Linh', 'Tran', FALSE, 'linh078@example.com', '0976543210', 'HCM City, Vietnam', 'linh078.jpg', 2);

-- Chèn thông tin cá nhân cho nhân viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, img_url, account_id) VALUES 
('STF2001', '567890123456', 'Duy', 'Le', TRUE, 'duy2001@example.com', '0965432109', 'Da Nang, Vietnam', 'duy2001.jpg', 3),
('STF2002', '678901234567', 'Anh', 'Pham', FALSE, 'anh2002@example.com', '0954321098', 'Can Tho, Vietnam', 'anh2002.jpg', 4);


-- Insert sample data for student
INSERT INTO student (id, class_id, is_studing) VALUES 
('N22DCCN127', 'D22CQCN02-N', TRUE), 
('N22DCCN078', 'D22CQCN01-N', TRUE);

-- Insert sample data for staff
INSERT INTO staff (id, is_working) VALUES 
('STF2001', TRUE), 
('STF2002', TRUE);

-- Insert sample data for penalty_form
INSERT INTO penalty_form (form_name, price) VALUES 
('Late Return', 50.00), 
('Damaged Equipment', 200.00);

-- Insert sample data for penalty_ticket
INSERT INTO penalty_ticket (staff_id, student_id, create_time, status) VALUES 
('STF2001', 'N22DCCN127', '2024-03-11 12:00:00', 'PENDING');

-- Insert sample data for violation
INSERT INTO violation (violation_content, penalty_form_id) VALUES 
('Late return of equipment', 1), 
('Damaged equipment', 2);

-- Insert sample data for detail_penalty_ticket
INSERT INTO detail_penalty_ticket (violation_id, penalty_ticket_id) VALUES 
(1, 1), 
(2, 1);

-- Insert sample data for repair_ticket
INSERT INTO repair_ticket (start_date, end_date, status, staff_id) VALUES 
('2024-03-10 10:00:00', NULL, 'PENDING', 'STF2002');

-- Insert sample data for detail_repair_ticket
INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, price) VALUES 
(1, 3, 100);

-- Insert sample data for disposal_form
INSERT INTO liquidation_slip (liquidation_date, staff_id) VALUES 
('2024-03-15', 'STF2001');

-- Insert sample data for detail_disposal_form
INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id) VALUES 
(1, 5);




INSERT INTO borrow_request (id, student_id, staff_id, status, borrowing_time, expect_returning_time) VALUES
(1, 'N22DCCN127', 'STF2001', 'ACCEPTED', '2024-04-01 6:30:00', '2024-04-07 10:40:00'),
(2, 'N22DCCN078', 'STF2001', 'RETURNED', '2024-03-25 07:00:00', '2024-03-30 10:40:00');

INSERT INTO borrow_item (borrow_request_id, equipment_id, actual_returning_time) VALUES
(1, 5, NULL), -- Mượn Microphone cho yêu cầu 1
(1, 6, NULL), -- Mượn Microphone khác cho yêu cầu 1
(1, 7, NULL),
(2, 11, '2024-03-30 10:30:00'), -- Trả Key cho yêu cầu 2
(2, 13, '2024-03-30 10:30:00'); -- Trả Key khác cho yêu cầu 2

/* VIEWS */
CREATE VIEW StudentInfo AS  
SELECT   
    s.id AS student_id,  
    p.id AS person_id,  
    a.id AS account_id,  
    s.class_id,  
    s.is_studing,  
    p.cccd,  
    p.first_name,  
    p.last_name,  
    p.gender,  
    p.email,  
    p.phone,  
    p.address,  
    p.img_url,  
    a.password,  
    a.role_id,  
    a.is_active  
FROM student AS s  
INNER JOIN person AS p ON s.id = p.id  
INNER JOIN account AS a ON p.account_id = a.id;

CREATE VIEW AccountInfo AS
SELECT
    p.id AS person_id,
    p.cccd,  
    p.first_name,  
    p.last_name,  
    p.gender,  
    p.email,  
    p.phone,  
    p.address,  
    p.img_url,
    a.password,  
    a.role_id,  
    a.is_active
FROM person AS p 
INNER JOIN account AS a ON p.account_id = a.id;

CREATE VIEW BorrowDetails AS
SELECT 
    br.id AS borrow_request_id,
    br.student_id,
    br.staff_id,
    br.status AS borrow_status,
    br.borrowing_time,
    br.expect_returning_time,
    bi.id AS borrow_item_id,
    bi.actual_returning_time,
    e.id AS equipment_id,
    e.equipment_name,
    e.status AS equipment_status,
    e.equipment_type,
    e.room_id
FROM borrow_request br
JOIN borrow_item bi ON br.id = bi.borrow_request_id
JOIN equipment e ON bi.equipment_id = e.id;

CREATE VIEW PenaltyDetails AS
SELECT 
    pt.id AS penalty_ticket_id,
    pt.staff_id,
    pt.student_id,
    pt.create_time,
    pt.status AS ticket_status,

    v.id AS violation_id,
    v.violation_content,

    pf.id AS penalty_form_id,
    pf.form_name,
    pf.price

FROM penalty_ticket pt
JOIN detail_penalty_ticket dpt ON pt.id = dpt.penalty_ticket_id
JOIN violation v ON dpt.violation_id = v.id
JOIN penalty_form pf ON v.penalty_form_id = pf.id;

/* PROCEDURE */

DELIMITER $$  

CREATE PROCEDURE CreateBorrowRequestWithItems(
    IN p_student_id VARCHAR(20),
    IN p_equipment_ids TEXT,  -- Danh sách các equipment_id, phân tách bằng dấu phẩy
    IN p_expect_returning_time DATETIME
)
BEGIN  
    DECLARE v_borrow_request_id INTEGER;
    DECLARE v_equipment_id INTEGER;
    DECLARE v_equipment_list TEXT;
    DECLARE v_equipment_pos INT;
    DECLARE v_equipment_len INT;
    
    -- 1. Tạo borrow_request
    INSERT INTO borrow_request (student_id, expect_returning_time) VALUES (p_student_id, p_expect_returning_time);
    SET v_borrow_request_id = LAST_INSERT_ID();

    -- 2. Duyệt từng equipment_id trong p_equipment_ids
    SET v_equipment_list = p_equipment_ids;

    WHILE LENGTH(v_equipment_list) > 0 DO
        -- Tìm vị trí dấu phẩy
        SET v_equipment_pos = LOCATE(',', v_equipment_list);
        
        IF v_equipment_pos = 0 THEN
            -- Nếu không còn dấu phẩy, lấy giá trị cuối cùng
            SET v_equipment_id = CAST(v_equipment_list AS UNSIGNED);
            SET v_equipment_list = '';
        ELSE
            -- Cắt lấy phần tử đầu tiên
            SET v_equipment_id = CAST(LEFT(v_equipment_list, v_equipment_pos - 1) AS UNSIGNED);
            SET v_equipment_list = SUBSTRING(v_equipment_list, v_equipment_pos + 1);
        END IF;
        
        -- Chèn vào borrow_item
        INSERT INTO borrow_item (borrow_request_id, equipment_id)
        VALUES (v_borrow_request_id, v_equipment_id);
    END WHILE;
END $$  
    
CREATE PROCEDURE accept_borrow_request(
    IN request_id INT,
    IN staff_id CHAR(10)
)
BEGIN
    -- Cập nhật trạng thái của thiết bị thành 'BORROWED'
    UPDATE equipment e
    JOIN borrow_item bi ON e.id = bi.equipment_id
    SET e.status = 'BORROWED'
    WHERE bi.borrow_request_id = request_id;

    -- Cập nhật trạng thái của yêu cầu mượn thành 'ACCEPTED'
    UPDATE borrow_request br
    SET br.status = 'ACCEPTED', br.staff_id = staff_id
    WHERE br.id = request_id;
    
END$$

CREATE PROCEDURE reject_borrow_request(
    IN request_id INT,
    IN staff_id CHAR(10)
)
BEGIN
    -- Cập nhật trạng thái của yêu cầu mượn thành 'REJECTED' và cập nhật staff_id
    UPDATE borrow_request br
    SET br.status = 'REJECTED', br.staff_id = staff_id
    WHERE br.id = request_id;

END$$


CREATE PROCEDURE change_equi_info(
    IN new_id INT,
    IN new_name CHAR(50),
    IN new_room CHAR(5)
)
BEGIN
    -- Cập nhật thiết bị
    UPDATE equipment e
    SET e.equipment_name = new_name, e.room_id = new_room
    WHERE  e.id=new_id;

END$$

CREATE PROCEDURE add_equipment(
    IN p_equipment_name VARCHAR(50),
    IN p_status ENUM('AVAILABLE', 'UNDERREPAIR', 'BORROWED', 'BROKEN', 'LIQUIDATED'),
    IN p_equipment_type ENUM('MOBILE', 'FIXED', 'SHARED'),
    IN p_room_id CHAR(5)
)
BEGIN
    -- Thêm thiết bị vào bảng equipment
    INSERT INTO equipment (equipment_name, status, equipment_type, room_id)
    VALUES (p_equipment_name, p_status, p_equipment_type, p_room_id);
END $$


CREATE PROCEDURE delete_equipment_by_id(
    IN p_equipment_id INT
)
BEGIN
    DECLARE max_id INT;

    -- Xóa thiết bị theo ID
    DELETE FROM equipment WHERE id = p_equipment_id;

    -- Cập nhật lại ID của các thiết bị còn lại để duy trì thứ tự liên tục
    UPDATE equipment 
    SET id = id - 1
    WHERE id > p_equipment_id;

    -- Lấy ID lớn nhất còn lại
    SELECT MAX(id) INTO max_id FROM equipment;

    -- Đặt lại AUTO_INCREMENT cho bảng equipment
    IF max_id IS NOT NULL THEN
        SET @query = CONCAT('ALTER TABLE equipment AUTO_INCREMENT = ', max_id + 1);
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    ELSE
        -- Nếu bảng trống, đặt AUTO_INCREMENT về 1
        ALTER TABLE equipment AUTO_INCREMENT = 1;
    END IF;

END $$

CREATE PROCEDURE return_equi(
    IN request_id INT
)
BEGIN
    -- Cập nhật trạng thái của thiết bị thành 'AVAILABLE'
    UPDATE equipment e
    JOIN borrow_item bi ON e.id = bi.equipment_id
    SET e.status = 'AVAILABLE'
    WHERE bi.borrow_request_id = request_id;

    -- Cập nhật trạng thái của yêu cầu mượn thành 'RETURNED'
    UPDATE borrow_request br
    SET br.status = 'RETURNED'
    WHERE br.id = request_id;
    
END$$


CREATE PROCEDURE get_all_repair_ticket()
BEGIN
    SELECT * FROM repair_ticket;
END$$



DELIMITER ; 



