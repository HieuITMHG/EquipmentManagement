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
    room_id CHAR(5) NOT NULL,
    borrowing_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expect_returning_time DATETIME NOT NULL,
    actual_returning_time DATETIME,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE borrow_item (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
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
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','COMPLETED') NOT NULL,
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
    FOREIGN KEY (penalty_ticket_id) REFERENCES penalty_ticket(id) ON DELETE CASCADE
);

CREATE TABLE repair_ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','COMPLETED') NOT NULL,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE detail_repair_ticket (
    repair_ticket_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    price INTEGER,
    PRIMARY KEY (repair_ticket_id, equipment_id),
    FOREIGN KEY (repair_ticket_id) REFERENCES repair_ticket(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

CREATE TABLE liquidation_slip (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    liquidation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED') NOT NULL,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE detail_liquidation_slip (
    liquidation_slip_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    PRIMARY KEY (liquidation_slip_id, equipment_id),
    FOREIGN KEY (liquidation_slip_id) REFERENCES liquidation_slip(id) ON DELETE CASCADE,
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
('Projector', 'BROKEN', 'FIXED', '2B25'), 
('Projector', 'AVAILABLE', 'FIXED', '2A16'), 
('Blackboard', 'AVAILABLE', 'FIXED', '2B25'), 
('Blackboard', 'AVAILABLE', 'FIXED', '2A16'), 
('Table', 'UNDERREPAIR', 'FIXED', '2B25'), 
('Table', 'AVAILABLE', 'FIXED', '2A16'), 
('Chair', 'AVAILABLE', 'FIXED', '2B25'), 
('Chair', 'BROKEN', 'FIXED', '2A16'), 
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
('Projector Remote', 'BROKEN', 'MOBILE', '2B25'), 
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

-- Chèn tài khoản cho quản lí
INSERT INTO account (password, role_id, is_active) VALUES 
('manager123', 1, TRUE),  -- Tài khoản cho 'MNG2000'

-- Chèn thông tin cá nhân cho sinh viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, img_url, account_id) VALUES 
('N22DCCN127', '123456789012', 'Hieu', 'Nguyen', TRUE, 'hieu127@example.com', '0987654321', 'Hanoi, Vietnam', 'hieu127.jpg', 1),
('N22DCCN078', '987654321012', 'Linh', 'Tran', FALSE, 'linh078@example.com', '0976543210', 'HCM City, Vietnam', 'linh078.jpg', 2);

-- Chèn thông tin cá nhân cho nhân viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, img_url, account_id) VALUES 
('STF2001', '567890123456', 'Duy', 'Le', TRUE, 'duy2001@example.com', '0965432109', 'Da Nang, Vietnam', 'duy2001.jpg', 3),
('STF2002', '678901234567', 'Anh', 'Pham', FALSE, 'anh2002@example.com', '0954321098', 'Can Tho, Vietnam', 'anh2002.jpg', 4);

-- Chèn thông tin cá nhân cho quản lí
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, img_url, account_id) VALUES 
('MNG2000', '678901234567', 'Dat', 'Vo', TRUE, 'dat2000@example.com', '0965432100', 'HCM City, Vietnam', 'duy2001.jpg', 5),

-- Insert sample data for student
INSERT INTO student (id, class_id, is_studing) VALUES 
('N22DCCN127', 'D22CQCN02-N', TRUE), 
('N22DCCN078', 'D22CQCN01-N', TRUE);

-- Insert sample data for staff
INSERT INTO staff (id, is_working) VALUES 
('STF2001', TRUE), 
('STF2002', TRUE),
('MNG2000', TRUE); --Quản lí

-- Insert sample data for penalty_form
INSERT INTO penalty_form (form_name, price) VALUES 
('Late Return', 50.00), 
('Damaged Equipment', 200.00);

-- Insert sample data for penalty_ticket
INSERT INTO penalty_ticket (staff_id, student_id, create_time, status) VALUES 
('STF2001', 'N22DCCN127', '2024-03-11 12:00:00', 'ACCEPTED');

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
('2024-03-15 10:00:00', NULL, 'PENDING', 'STF2002'); 

-- Insert sample data for detail_repair_ticket
INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, price) VALUES 
(1, 3, 100);

INSERT INTO repair_ticket (start_date, end_date, status, staff_id) VALUES 
('2024-04-01 09:30:00', '2024-04-05 15:00:00', 'COMPLETED', 'STF2001'),
('2025-05-01 09:45:00', '2025-05-02 15:00:00', 'ACCEPTED', 'STF2001');

-- Insert sample data for detail_repair_ticket (assumes this ticket has id = 2)
INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, price) VALUES 
(2, 5, 150),
(3, 7, 898831);

-- Insert sample data for disposal_form
INSERT INTO liquidation_slip (liquidation_date, staff_id, status) VALUES 
('2024-03-15', 'STF2001', 'ACCEPTED'),
('2024-4-5', 'STF2001', 'ACCEPTED');


-- Insert sample data for detail_disposal_form
INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id) VALUES 
(1, 5),
(2, 6);


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
    br.actual_returning_time,
    bi.id AS borrow_item_id,
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

CREATE VIEW v_liquidation_full_details AS
SELECT 
    ls.id AS liquidation_id,
    ls.liquidation_date,
    ls.status AS liquidation_status,
    ls.staff_id,
    dls.equipment_id,
    e.equipment_name,
    e.status AS equipment_status,
    e.equipment_type,
    e.room_id
FROM 
    liquidation_slip ls
INNER JOIN 
    detail_liquidation_slip dls
ON 
    ls.id = dls.liquidation_slip_id
INNER JOIN 
    equipment e
ON 
    dls.equipment_id = e.id;

CREATE VIEW v_repair_ticket_details AS
SELECT 
    rt.id AS repair_ticket_id,
    rt.start_date,
    rt.end_date,
    rt.status AS repair_ticket_status,
    rt.staff_id,
    drt.equipment_id,
    drt.price AS repair_price,
    e.equipment_name,
    e.status AS equipment_status,
    e.equipment_type,
    e.room_id
FROM 
    repair_ticket rt
INNER JOIN 
    detail_repair_ticket drt
ON 
    rt.id = drt.repair_ticket_id
INNER JOIN 
    equipment e
ON 
    drt.equipment_id = e.id;


/* PROCEDURE */

DELIMITER $$  

CREATE PROCEDURE CreateBorrowRequestWithItems(
    IN p_student_id VARCHAR(20),
    IN p_equipment_ids TEXT,  -- Danh sách các equipment_id, phân tách bằng dấu phẩy
    IN p_expect_returning_time DATETIME,
    IN p_room_id CHAR(5)
)
BEGIN  
    DECLARE v_borrow_request_id INTEGER;
    DECLARE v_equipment_id INTEGER;
    DECLARE v_equipment_list TEXT;
    DECLARE v_equipment_pos INT;
    DECLARE v_equipment_len INT;
    
    -- 1. Tạo borrow_request
    INSERT INTO borrow_request (student_id, expect_returning_time, room_id) VALUES (p_student_id, p_expect_returning_time, p_room_id);
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

        -- Cập nhật trạng thái của thiết bị thành 'PENDING'
        UPDATE equipment
        SET status = 'BORROWED'
        WHERE id = v_equipment_id;
    END WHILE;
END $$ 

CREATE PROCEDURE AddEquipmentsToBorrowRequest(
    IN p_borrow_request_id INTEGER,
    IN p_equipment_ids TEXT  -- Danh sách các equipment_id, phân tách bằng dấu phẩy
)
BEGIN
    DECLARE v_equipment_id INTEGER;
    DECLARE v_equipment_list TEXT;
    DECLARE v_equipment_pos INT;

    -- Khởi tạo danh sách thiết bị
    SET v_equipment_list = p_equipment_ids;

    -- Duyệt qua từng equipment_id trong danh sách
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

        -- Thêm thiết bị vào borrow_item
        INSERT INTO borrow_item (borrow_request_id, equipment_id)
        VALUES (p_borrow_request_id, v_equipment_id);

        -- Cập nhật trạng thái của thiết bị thành 'PENDING'
        UPDATE equipment 
        SET status = 'BORROWED'
        WHERE id = v_equipment_id;
    END WHILE;
END $$
    
CREATE PROCEDURE accept_borrow_request(
    IN request_id INT,
    IN staff_id CHAR(10)
)
BEGIN

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
    -- Cập nhật trạng thái của thiết bị thành 'BORROWED'
    UPDATE equipment e
    JOIN borrow_item bi ON e.id = bi.equipment_id
    SET e.status = 'AVAILABLE'
    WHERE bi.borrow_request_id = request_id;

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
    SET br.status = 'RETURNED',
        br.actual_returning_time = CURRENT_TIMESTAMP
    WHERE br.id = request_id;
    
END$$


CREATE PROCEDURE get_all_repair_ticket()
BEGIN
    SELECT * FROM repair_ticket;
END$$

CREATE PROCEDURE update_ticket_status_returned(
    IN p_ticket_id INT
)
BEGIN
    UPDATE repair_ticket
    SET status = 'RETURNED'
    WHERE id = p_ticket_id;
END $$

CREATE PROCEDURE check_equipment_in_room(IN room_id char(10), IN equipment_id VARCHAR(50))
BEGIN
    SELECT * FROM equipment
    WHERE id = equipment_id AND room_id = room_id;
END$$

CREATE PROCEDURE create_repair_ticket (
    IN in_staff_id CHAR(10),
    IN in_equipment_id VARCHAR(50),
    IN in_price INT,
    IN in_room_id CHAR(10)
)
BEGIN
    DECLARE new_ticket_id INT;

    -- 1. Kiểm tra thiết bị có đúng thuộc room không (tùy mục đích, có thể bỏ nếu không cần)
    IF EXISTS (
        SELECT 1 FROM equipment
        WHERE id = in_equipment_id AND room_id = in_room_id
    ) THEN
        -- 2. Tạo một repair_ticket mới
        INSERT INTO repair_ticket (staff_id, status)
        VALUES (in_staff_id, 'PENDING');

        -- 3. Lấy ID của ticket mới tạo
        SET new_ticket_id = LAST_INSERT_ID();

        -- 4. Thêm vào detail_repair_ticket
        INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, price)
        VALUES (new_ticket_id, in_equipment_id, in_price);

        -- 5. Cập nhật trạng thái thiết bị thành 'UNDERREPAIR'
        UPDATE equipment
        SET status = 'UNDERREPAIR'
        WHERE id = in_equipment_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Thiết bị không thuộc phòng đã chọn hoặc không tồn tại.';
    END IF;
END$$


CREATE PROCEDURE CreateLiquidationSlip(
    IN p_staff_id CHAR(10),
    IN p_equipment_ids TEXT,  -- Danh sách các equipment_id, phân tách bằng dấu phẩy
    IN p_role VARCHAR(10)     -- Tham số mới: 'staff' hoặc 'manager'
)
BEGIN  
    DECLARE v_liquidation_slip_id INTEGER;
    DECLARE v_equipment_id INTEGER;
    DECLARE v_pos INT;
    DECLARE v_status ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED');

    -- Xác định status dựa trên p_role
    SET v_status = CASE 
        WHEN p_role = 'staff' THEN 'PENDING'
        WHEN p_role = 'manager' THEN 'ACCEPTED'
        ELSE 'PENDING'  -- Giá trị mặc định nếu p_role không hợp lệ
    END;

    -- Tạo liquidation_slip với status
    INSERT INTO liquidation_slip (staff_id, status) 
    VALUES (p_staff_id, v_status);
    SET v_liquidation_slip_id = LAST_INSERT_ID();

    -- Xử lý danh sách equipment_ids
    WHILE LENGTH(p_equipment_ids) > 0 DO
        SET v_pos = LOCATE(',', p_equipment_ids);
        
        IF v_pos = 0 THEN
            SET v_equipment_id = CAST(p_equipment_ids AS UNSIGNED);
            SET p_equipment_ids = '';
        ELSE
            SET v_equipment_id = CAST(LEFT(p_equipment_ids, v_pos - 1) AS UNSIGNED);
            SET p_equipment_ids = SUBSTRING(p_equipment_ids, v_pos + 1);
        END IF;
        
        -- Chèn vào detail_liquidation_slip
        INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id)
        VALUES (v_liquidation_slip_id, v_equipment_id);

        UPDATE equipment
        SET status = 'LIQUIDATED'
        WHERE id = v_equipment_id;
    END WHILE;
END $$

CREATE PROCEDURE CreatePenaltyTicket(
    IN in_student_id CHAR(10),
    IN in_staff_id CHAR(10),
    IN in_violation_ids TEXT,
    IN p_role VARCHAR(20)
)
BEGIN
    DECLARE new_ticket_id INT;
    DECLARE current_violation_id INT;
    DECLARE ticket_status VARCHAR(20);

    -- Tắt yêu cầu khóa chính trong phiên làm việc
    SET SESSION sql_require_primary_key = 0;

    -- Xác định status dựa vào role
    IF p_role = 'manager' THEN
        SET ticket_status = 'ACCEPTED';
    ELSE
        SET ticket_status = 'PENDING';
    END IF;

    -- Xoá bảng tạm nếu đã tồn tại, rồi tạo mới
    DROP TEMPORARY TABLE IF EXISTS temp_violation_ids;
    CREATE TEMPORARY TABLE temp_violation_ids (id INT);

    -- Chèn các violation_id từ chuỗi TEXT vào bảng tạm
    WHILE LENGTH(in_violation_ids) > 0 DO
        SET current_violation_id = CAST(SUBSTRING_INDEX(in_violation_ids, ',', 1) AS UNSIGNED);
        INSERT INTO temp_violation_ids (id) VALUES (current_violation_id);
        
        -- Cắt phần tử đầu khỏi chuỗi
        IF LOCATE(',', in_violation_ids) > 0 THEN
            SET in_violation_ids = SUBSTRING(in_violation_ids, LOCATE(',', in_violation_ids) + 1);
        ELSE
            SET in_violation_ids = '';
        END IF;
    END WHILE;

    -- Tạo phiếu phạt mới
    INSERT INTO penalty_ticket (student_id, staff_id, status)
    VALUES (in_student_id, in_staff_id, ticket_status);

    SET new_ticket_id = LAST_INSERT_ID();

    -- Thêm chi tiết vi phạm
    INSERT INTO detail_penalty_ticket (violation_id, penalty_ticket_id)
    SELECT id, new_ticket_id FROM temp_violation_ids;

    -- Xoá bảng tạm
    DROP TEMPORARY TABLE IF EXISTS temp_violation_ids;
END $$

CREATE PROCEDURE CompleteRepairTicket(IN in_repair_ticket_id INT)
BEGIN
    -- Cập nhật trạng thái repair_ticket thành COMPLETED
    UPDATE repair_ticket
    SET status = 'COMPLETED'
    WHERE id = in_repair_ticket_id;

    -- Cập nhật trạng thái các thiết bị liên quan thành AVAILABLE
    UPDATE equipment
    SET status = 'AVAILABLE'
    WHERE id IN (
        SELECT equipment_id
        FROM detail_repair_ticket
        WHERE repair_ticket_id = in_repair_ticket_id
    );
END $$

CREATE PROCEDURE CompleteLiquidationSlip(IN in_liquidation_slip_id INT)
BEGIN
    -- Cập nhật trạng thái liquidation_slip thành COMPLETED
    UPDATE liquidation_slip
    SET status = 'COMPLETED'
    WHERE id = in_liquidation_slip_id;

    -- Cập nhật trạng thái các thiết bị liên quan thành AVAILABLE
    UPDATE equipment
    SET status = 'AVAILABLE'
    WHERE id IN (
        SELECT equipment_id
        FROM detail_liquidation_slip
        WHERE liquidation_slip_id = in_liquidation_slip_id
    );
END $$

DELIMITER ; 

/* TRIGGERS */
DELIMITER //

CREATE TRIGGER before_liquidation_slip_delete
BEFORE DELETE ON liquidation_slip
FOR EACH ROW
BEGIN
    -- Cập nhật status của equipment về AVAILABLE cho các thiết bị liên quan
    UPDATE equipment e
    INNER JOIN detail_liquidation_slip dls ON e.id = dls.equipment_id
    SET e.status = 'BROKEN'
    WHERE dls.liquidation_slip_id = OLD.id;
END //

CREATE TRIGGER before_repair_ticket_delete
BEFORE DELETE ON repair_ticket
FOR EACH ROW
BEGIN
    -- Cập nhật status của equipment về BROKEN cho các thiết bị liên quan
    UPDATE equipment e
    INNER JOIN detail_repair_ticket drt ON e.id = drt.equipment_id
    SET e.status = 'BROKEN'
    WHERE drt.repair_ticket_id = OLD.id;
END //


DELIMITER ;