DROP DATABASE IF EXISTS defaultdb;
CREATE DATABASE defaultdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use defaultdb;

/* CREATE TABLE SCRIPT */
-- Thiết lập mã hóa tiếng Việt
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Tạo bảng role
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng account
CREATE TABLE account (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    role_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng person
CREATE TABLE person (
    id VARCHAR(20) PRIMARY KEY,
    cccd CHAR(12) NOT NULL UNIQUE,
    first_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    last_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    gender BOOLEAN NOT NULL,
    email VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    phone CHAR(10) NOT NULL UNIQUE,
    address VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    account_id INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng department
CREATE TABLE department (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng class
CREATE TABLE class (
    id CHAR(20) PRIMARY KEY,
    class_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    academic_year CHAR(9) NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng room
CREATE TABLE room (
    id CHAR(5) PRIMARY KEY,
    floor_number INTEGER,
    section CHAR(1),
    max_people INTEGER
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng student
CREATE TABLE student (
    id VARCHAR(20) PRIMARY KEY,
    class_id CHAR(20) NOT NULL,
    is_studing BOOLEAN NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(id),
    FOREIGN KEY (id) REFERENCES person(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng staff
CREATE TABLE staff (
    id VARCHAR(20) PRIMARY KEY,
    is_working BOOLEAN NOT NULL,
    FOREIGN KEY (id) REFERENCES person(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE teacher (
    id VARCHAR(20) PRIMARY KEY,
    is_teaching BOOLEAN NOT NULL,
    FOREIGN KEY(id) REFERENCES person(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng equipment
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    equipment_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    status ENUM('AVAILABLE', 'UNDERREPAIR', 'BORROWED', 'BROKEN', 'LIQUIDATED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    equipment_type ENUM('MOBILE', 'FIXED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    room_id CHAR(5),
    quantity int DEFAULT 1,
    broken_quantity INT DEFAULT 0,
    under_repair_quantity INT DEFAULT 0,
    management_type ENUM('QUANTITY', 'INDIVIDUAL'),
    image_url varchar(200),
    FOREIGN KEY (room_id) REFERENCES room(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng borrow_request
CREATE TABLE borrow_request (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    person_id CHAR(10) NOT NULL,
    staff_id CHAR(10),
    status ENUM('PENDING', 'ACCEPTED', 'REJECTED','COMPLETED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING',
    room_id CHAR(5) NOT NULL,
    borrowing_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expect_returning_time DATETIME NOT NULL,
    actual_returning_time DATETIME,
    FOREIGN KEY (person_id) REFERENCES person(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng borrow_item
CREATE TABLE borrow_item (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    borrow_request_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (borrow_request_id) REFERENCES borrow_request(id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng repair_ticket
CREATE TABLE repair_ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,
    status ENUM('PREPARING','PENDING', 'ACCEPTED', 'REJECTED','COMPLETED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng detail_repair_ticket
CREATE TABLE detail_repair_ticket (
    repair_ticket_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    quantity INT DEFAULT 1,
    description VARCHAR(255),
    price DOUBLE,
    PRIMARY KEY (repair_ticket_id, equipment_id),
    FOREIGN KEY (repair_ticket_id) REFERENCES repair_ticket(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng liquidation_slip
CREATE TABLE liquidation_slip (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    liquidation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PREPARING','PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    staff_id CHAR(10) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng detail_liquidation_slip
CREATE TABLE detail_liquidation_slip (
    liquidation_slip_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    quantity INT DEFAULT 1,
    description VARCHAR(255),
    price DOUBLE,
    PRIMARY KEY (liquidation_slip_id, equipment_id),
    FOREIGN KEY (liquidation_slip_id) REFERENCES liquidation_slip(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE quarter (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    quarter_number TINYINT CHECK (quarter_number BETWEEN 1 AND 4),
    start_date DATE,
    end_date DATE
);

CREATE TABLE inventory_form (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_date DATE,
    end_date DATE,
    staff_id VARCHAR(20),
    quarter_id INT,
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    FOREIGN KEY (quarter_id) REFERENCES quarter(id)
);

CREATE TABLE detail_inventory_form (
    inventory_form_id INT AUTO_INCREMENT,
    room_id CHAR(5),
    total_devices INT,
    broken_count INT,
    repairing_count INT,
    liquidated_count INT,
    PRIMARY KEY (inventory_form_id, room_id),
    FOREIGN KEY (inventory_form_id) REFERENCES inventory_form(id),
    FOREIGN KEY (room_id) REFERENCES room(id)
);

/* INSERT SAMPLE DATA */
-- Insert sample data for role
INSERT INTO role (role_name) VALUES 
('Quản lý'), 
('Sinh viên'),
('Giảng viên'), 
('Sinh viên');

-- Insert sample data for department
INSERT INTO department (department_name) VALUES 
('Công nghệ thông tin'), 
('Điện tử viễn thông'), 
('Tài chính marketing');

-- Insert sample data for class
INSERT INTO class (id, class_name, academic_year, department_id) VALUES 
('D22CQCN02-N', 'Công nghệ thông tin 2', '2022-2027', 1), 
('D22CQQT01-N', 'Quản trị kinh doanh', '2022-2027', 1), 
('D22CQCN01-N', 'Công nghệ thông tin 1', '2022-2027', 2);

-- Insert sample data for room
INSERT INTO room (id, floor_number, section, max_people) VALUES 
('2B25', 2, 'B', 80), 
('2A16', 1, 'A', 100),
('2E21', 2, 'E', 50), 
('2B11', 1, 'B', 50),
('2B22', 2, 'B', 50),
('2E22', 2, 'E', 80),
('HVCS', NULL, NULL, NULL);

-- Thiết bị cố định cho phòng 2E22
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', '2E22', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', '2E22', 4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', '2E22', 20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', '2E22', 20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', '2E22', 2,'QUANTITY'),
('Máy chiếu', 'AVAILABLE', 'FIXED', '2E22', 1,'INDIVIDUAL');

-- Thiết bị cố định cho phòng 2B22
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', '2B22', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', '2B22', 4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', '2B22', 20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', '2B22', 20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', '2B22', 2, 'QUANTITY'),
('Máy chiếu', 'UNDERREPAIR', 'FIXED', '2B22', 1, 'INDIVIDUAL');

-- Thiết bị cố định cho phòng 2B11
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', '2B11', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', '2B11', 4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', '2B11', 20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', '2B11', 20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', '2B11', 2, 'QUANTITY'),
('Máy chiếu', 'AVAILABLE', 'FIXED', '2B11', 1, 'INDIVIDUAL');

-- Phòng 2A16
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', '2A16', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', '2A16', 4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', '2A16', 20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', '2A16', 20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', '2A16', 2, 'QUANTITY'),
('Máy chiếu', 'AVAILABLE', 'FIXED', '2A16', 1, 'INDIVIDUAL');


-- Phòng 2E21
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', '2E21', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', '2E21', 4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', '2E21', 20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', '2E21', 20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', '2E21', 2, 'QUANTITY'),
('Máy chiếu', 'AVAILABLE', 'FIXED', '2E21', 1, 'INDIVIDUAL');

-- Thiết bị cố định cho tất cả các phòng
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, quantity, management_type) VALUES 
('Máy điều hòa', 'AVAILABLE', 'FIXED', 'HVCS', 3, 'QUANTITY'),
('Quạt trần', 'AVAILABLE', 'FIXED', 'HVCS',4, 'QUANTITY'),
('Bàn', 'AVAILABLE', 'FIXED', 'HVCS',20, 'QUANTITY'),
('Ghế', 'AVAILABLE', 'FIXED', 'HVCS',20, 'QUANTITY'),
('Bảng đen', 'AVAILABLE', 'FIXED', 'HVCS',2, 'QUANTITY'),
('Máy chiếu', 'AVAILABLE', 'FIXED', 'HVCS',1, 'INDIVIDUAL');

-- Thiết bị di động phòng 2E22
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/remote.png'),
('Micro không dây', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2E22','INDIVIDUAL', 'img/lazer_pen.png');

-- Thiết bị di động phòng 2B22
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/remote.png'),
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/lazer_pen.png');

-- Thiết bị di động phòng 2B11
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/remote.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/lazer_pen.png');

-- Thiết bị di động cho mỗi phòng
-- 2B25
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/lazer_pen.png');

-- 2A16
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/remote.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/lazer_pen.png');

-- 2E21
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/lazer_pen.png');

-- 2E22 (bạn đã có đoạn này rồi, mình skip)

-- 2B22 (lặp lại)
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/remote.png');

-- 2B11 (lặp lại)
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/lazer_pen.png');

-- Thiết bị dùng chung
INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
('Micro không dây', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE','MOBILE','HVCS', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Micro không dây', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE', 'HVCS', 'INDIVIDUAL', 'img/lazer_pen.png'),
('Micro không dây', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/micro.png'),
('Điều khiển máy chiếu', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/remote.png'),
('Bút laser', 'AVAILABLE', 'MOBILE','HVCS', 'INDIVIDUAL', 'img/lazer_pen.png');

INSERT INTO equipment (equipment_name, status, equipment_type, room_id, management_type, image_url) VALUES 
-- Phòng 2B25
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B25', 'INDIVIDUAL', 'img/key.png'),

-- Phòng 2A16
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2A16', 'INDIVIDUAL', 'img/key.png'),

-- Phòng 2E21
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2E21', 'INDIVIDUAL', 'img/key.png'),

-- Phòng 2E22
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2E22', 'INDIVIDUAL', 'img/key.png'),

-- Phòng 2B22
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B22', 'INDIVIDUAL', 'img/key.png'),

-- Phòng 2B11
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/key.png'),
('Chìa khóa', 'AVAILABLE', 'MOBILE', '2B11', 'INDIVIDUAL', 'img/key.png');


-- Chèn tài khoản cho sinh viên
INSERT INTO account (password, role_id, is_active) VALUES 
('student123', 4, TRUE),  -- Tài khoản cho 'N22DCCN127'
('student456', 4, TRUE);  -- Tài khoản cho 'N22DCCN078'

-- Chèn tài khoản cho nhân viên
INSERT INTO account (password, role_id, is_active) VALUES 
('staff123', 2, TRUE),  -- Tài khoản cho 'STF2001'
('staff456', 2, TRUE);  -- Tài khoản cho 'STF2002'

-- Chèn thông tin cá nhân cho sinh viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, account_id) VALUES 
('N22DCCN127', '123456789012', 'Hieu', 'Nguyen', TRUE, 'hieu127@example.com', '0987654321', 'Hanoi, Vietnam', 1),
('N22DCCN078', '987654321012', 'Linh', 'Tran', FALSE, 'linh078@example.com', '0976543210', 'HCM City, Vietnam', 2);

-- Chèn thông tin cá nhân cho nhân viên
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, account_id) VALUES 
('STF2001', '567890123456', 'Duy', 'Le', TRUE, 'duy2001@example.com', '0965432109', 'Da Nang, Vietnam', 3),
('STF2002', '678901234567', 'Anh', 'Pham', FALSE, 'anh2002@example.com', '0954321098', 'Can Tho, Vietnam', 4);

-- Insert sample data for student
INSERT INTO student (id, class_id, is_studing) VALUES 
('N22DCCN127', 'D22CQCN02-N', TRUE), 
('N22DCCN078', 'D22CQCN01-N', TRUE);

-- Insert sample data for staff
INSERT INTO staff (id, is_working) VALUES 
('STF2001', TRUE), 
('STF2002', TRUE);

INSERT INTO account (password, role_id, is_active) VALUES
('QL001', 1, TRUE); 
INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, account_id) VALUES 
('QL001', '635945826578', 'Sang', 'Tran', TRUE, 'sangtran127@example.com', '4333244521', 'Hanoi, Vietnam', 5);
INSERT INTO staff (id, is_working) VALUES 
('QL001', TRUE);

-- Insert sample data for disposal_form
INSERT INTO liquidation_slip (liquidation_date, staff_id, status) VALUES 
('2024-03-15', 'STF2001', 'ACCEPTED'),
('2024-4-5', 'STF2001', 'ACCEPTED');

-- Insert sample data for detail_disposal_form
INSERT INTO detail_liquidation_slip (liquidation_slip_id, equipment_id) VALUES 
(1, 5),
(2, 6);

INSERT INTO quarter (year, quarter_number, start_date, end_date) VALUES
(2023, 2, '2023-07-01', '2023-12-31'),
(2024, 1, '2024-01-01', '2024-06-30'),
(2024, 2, '2024-07-01', '2024-12-31');
INSERT INTO inventory_form (start_date, end_date, staff_id, quarter_id) VALUES
('2023-07-05', '2023-07-10', 'STF2001', 1),
('2024-01-07', '2024-01-12', 'STF2001', 2),
('2024-07-01', '2024-07-05', 'STF2001', 3);

-- Quý 1
INSERT INTO detail_inventory_form (inventory_form_id, room_id, total_devices, broken_count, repairing_count, liquidated_count) VALUES
(1, '2B25', 80, 2, 1, 0),
(1, '2A16', 100, 0, 0, 1),
(1, '2E21', 50, 1, 0, 0),
(1, '2B11', 50, 0, 1, 1),
(1, '2B22', 50, 0, 0, 0),
(1, '2E22', 80, 1, 1, 0),
(1, 'HVCS', 0, 0, 0, 0);

-- Quý 2
INSERT INTO detail_inventory_form(inventory_form_id, room_id, total_devices, broken_count, repairing_count, liquidated_count) VALUES
(2, '2B25', 80, 1, 1, 1),
(2, '2A16', 100, 0, 0, 0),
(2, '2E21', 50, 0, 2, 0),
(2, '2B11', 50, 0, 0, 0),
(2, '2B22', 50, 1, 0, 0),
(2, '2E22', 80, 2, 1, 1),
(2, 'HVCS', 0, 0, 0, 0);

-- Quý 3
INSERT INTO detail_inventory_form (inventory_form_id, room_id, total_devices, broken_count, repairing_count, liquidated_count) VALUES
(3, '2B25', 80, 0, 0, 0),
(3, '2A16', 100, 1, 0, 0),
(3, '2E21', 50, 0, 0, 1),
(3, '2B11', 50, 0, 1, 0),
(3, '2B22', 50, 0, 0, 0),
(3, '2E22', 80, 1, 0, 1),
(3, 'HVCS', 0, 0, 0, 0);


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
    a.password,  
    a.role_id,  
    a.is_active
FROM person AS p 
INNER JOIN account AS a ON p.account_id = a.id;

CREATE VIEW BorrowDetails AS
SELECT 
    br.id AS borrow_request_id,
    br.person_id,
    br.staff_id,
    br.status AS borrow_status,
    br.borrowing_time,
    br.expect_returning_time,
    br.actual_returning_time,
    br.room_id AS borrow_room_id,
    bi.id AS borrow_item_id,
    e.id AS equipment_id,
    e.equipment_name,
    e.status AS equipment_status,
    e.equipment_type,
    e.room_id,
    e.image_url
FROM borrow_request br
JOIN borrow_item bi ON br.id = bi.borrow_request_id
JOIN equipment e ON bi.equipment_id = e.id;

CREATE VIEW v_liquidation_full_details AS
SELECT 
    ls.id AS liquidation_id,
    ls.liquidation_date,
    ls.status AS liquidation_status,
    ls.staff_id,
    dls.equipment_id,
    dls.price AS income,
    dls.description,
    dls.quantity,
    e.id AS e_id,
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
    drt.description,
    drt.quantity,
    e.id AS e_id,
    e.equipment_name,
    e.status AS equipment_status,
    e.equipment_type,
    e.room_id,
    e.image_url
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

CREATE VIEW inventory_summary AS
SELECT
    q.id AS quarter_id,
    q.year AS quarter_year,
    q.quarter_number AS quarter_number,
    q.start_date AS quarter_start_date,
    q.end_date AS quarter_end_date,
    i.id AS inventory_form_id,
    i.start_date AS inventory_start_date,
    i.end_date AS inventory_end_date,
    i.staff_id,
    d.room_id,
    d.total_devices,
    d.broken_count,
    d.repairing_count,
    d.liquidated_count
FROM
    quarter q
JOIN
    inventory_form i ON q.id = i.quarter_id
JOIN
    detail_inventory_form d ON i.id = d.inventory_form_id;



/* PROCEDURE */

DELIMITER $$  

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

CREATE PROCEDURE cancel_borrow_equipment(
    IN p_equipment_id INT,
    IN p_borrow_request_id INT
)
BEGIN
    -- Xóa bản ghi tương ứng trong bảng borrow_item
    DELETE FROM borrow_item
    WHERE equipment_id = p_equipment_id AND borrow_request_id = p_borrow_request_id;

    -- Cập nhật trạng thái thiết bị thành AVAILABLE
    UPDATE equipment
    SET status = 'AVAILABLE'
    WHERE id = p_equipment_id;

    -- Kiểm tra xem borrow_request còn borrow_item nào không
    IF NOT EXISTS (
        SELECT 1 FROM borrow_item WHERE borrow_request_id = p_borrow_request_id
    ) THEN
        -- Nếu không còn thì xóa luôn borrow_request
        DELETE FROM borrow_request
        WHERE id = p_borrow_request_id;
    END IF;
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


CREATE PROCEDURE update_equipment_info (
    IN p_id INT,
    IN p_equipment_name VARCHAR(50),
    IN p_status ENUM('AVAILABLE', 'UNDERREPAIR', 'BORROWED', 'BROKEN', 'LIQUIDATED'),
    IN p_room_id CHAR(5),
    IN p_image_url VARCHAR(200)
)
BEGIN
    UPDATE equipment
    SET
        equipment_name = p_equipment_name,
        status = p_status,
        room_id = p_room_id,
        image_url = COALESCE(p_image_url, image_url)
    WHERE id = p_id;
END$$

CREATE PROCEDURE create_equipment (
    IN p_equipment_name VARCHAR(50),
    IN p_equipment_type ENUM('MOBILE', 'FIXED'),
    IN p_management_type ENUM('QUANTITY', 'INDIVIDUAL'),
    IN p_room_id CHAR(5),
    IN p_quantity INT,
    IN p_image_url VARCHAR(200)
)
BEGIN
    INSERT INTO equipment (
        equipment_name,
        status,
        equipment_type,
        management_type,
        room_id,
        quantity,
        broken_quantity,
        under_repair_quantity,
        image_url
    ) VALUES (
        p_equipment_name,
        'AVAILABLE',             -- Status mặc định là AVAILABLE khi mới thêm
        p_equipment_type,
        p_management_type,       -- Bây giờ thêm cả management_type
        p_room_id,
        p_quantity,
        0,                       -- broken_quantity mặc định 0
        0,                       -- under_repair_quantity mặc định 0
        p_image_url
    );
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
    SET br.status = 'COMPLETED',
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
    IN in_equipment_price_str TEXT,
    IN in_role VARCHAR(50)
)
BEGIN
    DECLARE new_ticket_id INT;
    DECLARE equipment_price_pair TEXT;
    DECLARE equipment_id INT;
    DECLARE price_value INT;
    DECLARE pos INT DEFAULT 1;
    DECLARE status_val VARCHAR(20);

    -- Xác định trạng thái dựa vào vai trò
    IF in_role = 'staff' THEN
        SET status_val = 'PENDING';
    ELSEIF in_role = 'manager' THEN
        SET status_val = 'ACCEPTED';
    ELSE
        -- Mặc định nếu role không hợp lệ
        SET status_val = 'PENDING';
    END IF;

    -- Tạo ticket
    INSERT INTO repair_ticket (staff_id, status)
    VALUES (in_staff_id, status_val);

    SET new_ticket_id = LAST_INSERT_ID();

    -- Lặp qua từng cặp equipment:price
    WHILE LENGTH(in_equipment_price_str) > 0 DO
        SET pos = LOCATE(',', in_equipment_price_str);

        IF pos = 0 THEN
            SET equipment_price_pair = in_equipment_price_str;
            SET in_equipment_price_str = '';
        ELSE
            SET equipment_price_pair = SUBSTRING(in_equipment_price_str, 1, pos - 1);
            SET in_equipment_price_str = SUBSTRING(in_equipment_price_str, pos + 1);
        END IF;

        SET equipment_id = CAST(SUBSTRING_INDEX(equipment_price_pair, ':', 1) AS UNSIGNED);
        SET price_value = CAST(SUBSTRING_INDEX(equipment_price_pair, ':', -1) AS UNSIGNED);

        INSERT INTO detail_repair_ticket (repair_ticket_id, equipment_id, price)
        VALUES (new_ticket_id, equipment_id, price_value);

        UPDATE equipment
        SET status = 'UNDERREPAIR'
        WHERE id = equipment_id;
    END WHILE;
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

CREATE PROCEDURE CompleteRepairTicket(IN in_repair_ticket_id INT)
BEGIN
    -- Cập nhật trạng thái và thời gian kết thúc của repair_ticket thành COMPLETED và thời điểm hiện tại
    UPDATE repair_ticket
    SET 
        status = 'COMPLETED',
        end_date = CURRENT_TIMESTAMP
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

CREATE PROCEDURE CreateNewAccount(
    IN p_cccd CHAR(12),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_gender BOOLEAN,
    IN p_email VARCHAR(100),
    IN p_phone CHAR(10),
    IN p_address VARCHAR(255),
    IN p_role_id INTEGER,
    IN p_class_id CHAR(20),
    IN p_account_code VARCHAR(50),
    IN p_password VARCHAR(500)
)
BEGIN
    DECLARE new_account_id INTEGER;
    DECLARE exit handler for SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Lỗi khi tạo tài khoản mới';
    END;

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Chèn vào bảng account
    INSERT INTO account (password, role_id, is_active)
    VALUES (p_password, p_role_id, TRUE);
    
    -- Lấy account_id vừa tạo
    SET new_account_id = LAST_INSERT_ID();

    -- Chèn vào bảng person
    INSERT INTO person (id, cccd, first_name, last_name, gender, email, phone, address, account_id)
    VALUES (p_account_code, p_cccd, p_first_name, p_last_name, p_gender, p_email, p_phone, p_address, new_account_id);

    -- Kiểm tra role_id để chèn vào bảng student hoặc staff
    IF p_role_id = 2 THEN
        -- Sinh viên: chèn vào bảng student
        IF p_class_id IS NULL THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Class_id không được để trống cho sinh viên';
        END IF;
        
        INSERT INTO student (id, class_id, is_studing)
        VALUES (p_account_code, p_class_id, TRUE);
    ELSEIF p_role_id = 1 OR p_role_id = 3 THEN
        -- Manager hoặc Staff: chèn vào bảng staff
        INSERT INTO staff (id, is_working)
        VALUES (p_account_code, TRUE);
    END IF;

    -- Hoàn tất giao dịch
    COMMIT;
END $$

CREATE PROCEDURE UpdateAccount(
    IN p_person_id VARCHAR(20),
    IN p_cccd CHAR(12),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_gender BOOLEAN,
    IN p_email VARCHAR(100),
    IN p_phone CHAR(10),
    IN p_address VARCHAR(255),
    IN p_role_id INTEGER,
    IN p_class_id CHAR(20),
    IN p_is_studing BOOLEAN,
    IN p_is_working BOOLEAN
)
BEGIN
    DECLARE account_id INTEGER;
    DECLARE exit handler for SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Lỗi khi cập nhật tài khoản';
    END;

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Lấy account_id
    SELECT account_id INTO account_id
    FROM person
    WHERE id = p_person_id;

    -- Cập nhật bảng person
    UPDATE person
    SET 
        cccd = p_cccd,
        first_name = p_first_name,
        last_name = p_last_name,
        gender = p_gender,
        email = p_email,
        phone = p_phone,
        address = p_address
    WHERE id = p_person_id;

    -- Cập nhật role_id trong bảng account
    UPDATE account
    SET role_id = p_role_id
    WHERE id = account_id;

    -- Xử lý theo role_id
    IF p_role_id = 2 THEN
        -- Sinh viên: cập nhật hoặc chèn vào bảng student
        IF EXISTS (SELECT 1 FROM student WHERE id = p_person_id) THEN
            UPDATE student
            SET class_id = p_class_id, is_studing = p_is_studing
            WHERE id = p_person_id;
        ELSE
            INSERT INTO student (id, class_id, is_studing)
            VALUES (p_person_id, p_class_id, p_is_studing);
        END IF;
    ELSEIF p_role_id = 1 OR p_role_id = 3 THEN
        -- Manager hoặc Staff: cập nhật hoặc chèn vào bảng staff
        IF EXISTS (SELECT 1 FROM staff WHERE id = p_person_id) THEN
            UPDATE staff
            SET is_working = p_is_working
            WHERE id = p_person_id;
        ELSE
            INSERT INTO staff (id, is_working)
            VALUES (p_person_id, p_is_working);
        END IF;
    END IF;

    -- Hoàn tất giao dịch
    COMMIT;
END $$

CREATE PROCEDURE DeleteAccount(
    IN p_person_id VARCHAR(20)
)
BEGIN
    DECLARE account_id INTEGER;
    DECLARE exit handler for SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Orror when try to delete account';
    END;

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Lấy account_id
    SELECT account_id INTO account_id
    FROM person
    WHERE id = p_person_id;

    -- Xóa khỏi student hoặc staff
    DELETE FROM student WHERE id = p_person_id;
    DELETE FROM staff WHERE id = p_person_id;

    -- Xóa khỏi person
    DELETE FROM person WHERE id = p_person_id;

    -- Xóa khỏi account
    DELETE FROM account WHERE id = account_id;

    -- Hoàn tất giao dịch
    COMMIT;
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

CREATE TRIGGER equipment_status_update
BEFORE UPDATE ON equipment
FOR EACH ROW
BEGIN
    IF NEW.management_type = 'INDIVIDUAL' THEN
        IF NEW.status = 'BROKEN' THEN
            SET NEW.broken_quantity = 1;
            SET NEW.under_repair_quantity = 0;
        ELSEIF NEW.status = 'UNDERREPAIR' THEN
            SET NEW.under_repair_quantity = 1;
            SET NEW.broken_quantity = 0;
        ELSE
            SET NEW.broken_quantity = 0;
            SET NEW.under_repair_quantity = 0;
        END IF;
    END IF;
END;//

DELIMITER ;
