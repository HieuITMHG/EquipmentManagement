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
    staff_id CHAR(10) NOT NULL,
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

CREATE TABLE borrow_item (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    borrowing_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expect_returning_time DATETIME NOT NULL,
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
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED') NOT NULL,
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
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED') NOT NULL,
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
('2A16', 1, 'A', 100);

-- Insert sample data for fixed equipment (each room has one speaker and one projector)
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
('Speaker', 'AVAILABLE', 'FIXED', '2B25'), 
('Speaker', 'AVAILABLE', 'FIXED', '2A16'), 
('Projector', 'AVAILABLE', 'FIXED', '2B25'), 
('Projector', 'AVAILABLE', 'FIXED', '2A16');

-- Insert sample data for mobile equipment (each room gets 2 microphones, 2 keys, 2 remotes)
INSERT INTO equipment (equipment_name, status, equipment_type, room_id) VALUES 
-- Equipment for Room 2B25
('Microphone', 'AVAILABLE', 'MOBILE', '2B25'), 
('Microphone', 'AVAILABLE', 'MOBILE', '2B25'), 
('Key', 'AVAILABLE', 'MOBILE', '2B25'), 
('Key', 'AVAILABLE', 'MOBILE', '2B25'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2B25'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2B25'), 

-- Equipment for Room 2A16
('Microphone', 'AVAILABLE', 'MOBILE', '2A16'), 
('Microphone', 'AVAILABLE', 'MOBILE', '2A16'), 
('Key', 'AVAILABLE', 'MOBILE', '2A16'), 
('Key', 'AVAILABLE', 'MOBILE', '2A16'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2A16'), 
('Projector Remote', 'AVAILABLE', 'MOBILE', '2A16');

-- Chèn tài khoản cho sinh viên
INSERT INTO account (password, role_id, is_active) VALUES 
('student123', 2, TRUE),  -- Tài khoản cho 'N22DCCN127'
('student456', 2, TRUE);  -- Tài khoản cho 'N22DCCN078'

-- Chèn tài khoản cho nhân viên
INSERT INTO account (password, role_id, is_active) VALUES 
('staff123', 1, TRUE),  -- Tài khoản cho 'STF2001'
('staff456', 1, TRUE);  -- Tài khoản cho 'STF2002'

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

-- Insert sample data for borrow_request
INSERT INTO borrow_request (student_id, staff_id, status) VALUES 
('N22DCCN127', 'STF2001', 'PENDING'), 
('N22DCCN078', 'STF2002', 'ACCEPTED');

-- Insert sample data for borrow_item
INSERT INTO borrow_item (borrowing_time, expect_returning_time, actual_returning_time, borrow_request_id, equipment_id) VALUES 
('2024-03-10 10:00:00', '2024-03-12 10:00:00', NULL, 1, 1), 
('2024-03-11 09:00:00', '2024-03-13 09:00:00', NULL, 2, 2);

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

/* PROCEDURE */

DELIMITER $$  
CREATE PROCEDURE GetStudentInfoById(IN studentId VARCHAR(20))  
BEGIN  
    SELECT   
        s.id AS student_id,  
        p.id AS person_id,  
        a.id AS account_id,  
        s.*,  
        p.*,  
        a.*  
    FROM student AS s  
    INNER JOIN person AS p ON s.id = p.id  
    INNER JOIN account AS a ON p.account_id = a.id  
    WHERE s.id = studentId;  
END $$  
DELIMITER ;  


