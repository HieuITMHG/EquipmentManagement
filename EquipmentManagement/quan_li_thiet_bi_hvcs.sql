DROP DATABASE IF EXISTS thiet_bi_hvcs;

CREATE DATABASE thiet_bi_hvcs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

USE thiet_bi_hvcs;

-- Tạo bảng vai_tro
CREATE TABLE vai_tro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ten_vai_tro VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng lop
CREATE TABLE lop (
    id VARCHAR(20) PRIMARY KEY,
    ten_lop VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE,
    nien_khoa CHAR(9)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng phong
CREATE TABLE phong (
    id CHAR(5) PRIMARY KEY,
    suc_chua INT DEFAULT 40,
    tang TINYINT,
    khu CHAR(1)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng tai_khoan
CREATE TABLE tai_khoan (
    id VARCHAR(20) PRIMARY KEY,
    mat_khau VARCHAR(500),
    vai_tro_id INT NOT NULL,
    dang_hoat_dong BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (vai_tro_id) REFERENCES vai_tro(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng sinh_vien
CREATE TABLE sinh_vien (
    id VARCHAR(20) PRIMARY KEY,
    lop_id VARCHAR(20) NOT NULL,
    cccd CHAR(12) UNIQUE,
    ho VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    ten VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    gioi_tinh BOOLEAN NOT NULL,
    email VARCHAR(100) UNIQUE,
    sdt CHAR(10) UNIQUE,
    dia_chi VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    dang_hoc BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(id) REFERENCES tai_khoan(id),
    FOREIGN KEY(lop_id) REFERENCES lop(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng nhan_vien
CREATE TABLE nhan_vien (
    id VARCHAR(20) PRIMARY KEY,
    cccd CHAR(12) UNIQUE,
    ho VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    ten VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    gioi_tinh BOOLEAN NOT NULL,
    email VARCHAR(100) UNIQUE,
    sdt CHAR(10) UNIQUE,
    dia_chi VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    dang_lam_viec BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(id) REFERENCES tai_khoan(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng thiet_bi
CREATE TABLE thiet_bi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ten_thiet_bi VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    trang_thai ENUM('CO_SAN', 'DANG_BAO_TRI', 'DANG_MUON', 'HU_HONG', 'DA_THANH_LY', 'DA_MAT') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CO_SAN',
    loai_thiet_bi ENUM('DI_DONG', 'CO_DINH') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    phong_id CHAR(5) NOT NULL,
    anh VARCHAR(50),
    FOREIGN KEY(phong_id) REFERENCES phong(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng phieu_muon
CREATE TABLE phieu_muon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sinh_vien_id VARCHAR(20) NOT NULL,
    nhan_vien_id VARCHAR(20),
    phong_id CHAR(5) NOT NULL,
    ca TIMESTAMP NOT NULL,
    thoi_gian_tra_du_kien TIMESTAMP NOT NULL,
    trang_thai ENUM('CHO_DUYET', 'DA_DUYET') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CHO_DUYET',
    FOREIGN KEY (sinh_vien_id) REFERENCES sinh_vien(id),
    FOREIGN KEY (nhan_vien_id) REFERENCES nhan_vien(id),
    FOREIGN KEY (phong_id) REFERENCES phong(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng chi_tiet_muon
CREATE TABLE chi_tiet_muon (
    thoi_gian_muon TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    thoi_gian_tra_thuc_te DATETIME,
    phieu_muon_id INT,
    thiet_bi_id INT,
    PRIMARY KEY (phieu_muon_id, thiet_bi_id),
    FOREIGN KEY (phieu_muon_id) REFERENCES phieu_muon(id) ON DELETE CASCADE,
    FOREIGN KEY (thiet_bi_id) REFERENCES thiet_bi(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng phieu_sua_chua
CREATE TABLE phieu_sua_chua (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ngay_bat_dau TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_ket_thuc TIMESTAMP,
    trang_thai ENUM('CHUAN_BI','CHO_DUYET', 'DA_DUYET', 'HOAN_THANH') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CHO_DUYET',
    nhan_vien_id VARCHAR(20) NOT NULL,
    FOREIGN KEY(nhan_vien_id) REFERENCES nhan_vien(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng chi_tiet_sua_chua
CREATE TABLE chi_tiet_sua_chua (
    phieu_sua_chua_id INT NOT NULL,
    thiet_bi_id INT NOT NULL,
    gia DOUBLE DEFAULT 0,
    ghi_chu TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    PRIMARY KEY(phieu_sua_chua_id, thiet_bi_id),
    FOREIGN KEY(phieu_sua_chua_id) REFERENCES phieu_sua_chua(id) ON DELETE CASCADE,
    FOREIGN KEY(thiet_bi_id) REFERENCES thiet_bi(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng phieu_thanh_ly
CREATE TABLE phieu_thanh_ly (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ngay_thanh_ly TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    trang_thai ENUM('CHUAN_BI','CHO_DUYET', 'DA_DUYET', 'HOAN_THANH') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CHO_DUYET',
    nhan_vien_id VARCHAR(20) NOT NULL,
    FOREIGN KEY(nhan_vien_id) REFERENCES nhan_vien(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng chi_tiet_thanh_ly
CREATE TABLE chi_tiet_thanh_ly (
    phieu_thanh_ly_id INT NOT NULL,
    thiet_bi_id INT NOT NULL,
    gia DOUBLE DEFAULT 0,
    ghi_chu TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    PRIMARY KEY(phieu_thanh_ly_id, thiet_bi_id),
    FOREIGN KEY(phieu_thanh_ly_id) REFERENCES phieu_thanh_ly(id) ON DELETE CASCADE,
    FOREIGN KEY(thiet_bi_id) REFERENCES thiet_bi(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng phieu_kiem_ke
CREATE TABLE phieu_kiem_ke (
    id INT PRIMARY KEY AUTO_INCREMENT,
    thoi_gian_bat_dau TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    thoi_gian_ket_thuc TIMESTAMP,
    nhan_vien_id VARCHAR(20) NOT NULL,
    FOREIGN KEY(nhan_vien_id) REFERENCES nhan_vien(id)
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Tạo bảng chi_tiet_kiem_ke
CREATE TABLE chi_tiet_kiem_ke (
  phieu_kiem_ke_id INT NOT NULL,
  phong_id CHAR(5) NOT NULL,
  tong_so INT NOT NULL,
  ghi_chu VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  so_luong_hong INT DEFAULT 0,
  so_luong_sua_chua INT DEFAULT 0,
  so_luong_thanh_ly INT DEFAULT 0,
  PRIMARY KEY(phieu_kiem_ke_id, phong_id),
  FOREIGN KEY(phieu_kiem_ke_id) REFERENCES phieu_kiem_ke(id),
  FOREIGN KEY(phong_id) REFERENCES phong(id),
  CHECK (tong_so >= 0),
  CHECK (so_luong_hong >= 0),
  CHECK (so_luong_sua_chua >= 0),
  CHECK (so_luong_thanh_ly >= 0),
  CHECK (
    so_luong_hong + so_luong_sua_chua + so_luong_thanh_ly <= tong_so
  )
) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

INSERT INTO vai_tro (ten_vai_tro) VALUES
('Quản lý'),
('Nhân viên quản lý thiết bị'),
('Sinh viên');

INSERT INTO lop (id, ten_lop, nien_khoa) VALUES
('L01', 'CNTT01', '2023-2026'),
('L02', 'CNTT02', '2023-2026'),
('L03', 'KTPM01', '2023-2026');

INSERT INTO phong (id, suc_chua, tang, khu) VALUES
('P101', 40, 1, 'A'),
('P102', 50, 1, 'A'),
('P201', 40, 2, 'B');

INSERT INTO tai_khoan (id, mat_khau, vai_tro_id, dang_hoat_dong) VALUES
('SV001', '123', 3, TRUE),
('SV002', '123', 3, TRUE),
('SV003', '123', 3, TRUE),
('NV001', '123', 2, TRUE),
('NV002', '123', 2, TRUE),
('AD001', '123', 1, TRUE);

INSERT INTO sinh_vien (id, lop_id, cccd, ho, ten, gioi_tinh, email, sdt, dia_chi, dang_hoc) VALUES
('SV001', 'L01', '123456689001', 'Nguyen', 'Van A', TRUE, 'sv001@email.com', '0901234001', 'Hanoi', TRUE),
('SV002', 'L02', '123456689002', 'Tran', 'Thi B', FALSE, 'sv002@email.com', '0901234002', 'Hanoi', TRUE),
('SV003', 'L03', '123456689003', 'Le', 'Van C', TRUE, 'sv003@email.com', '0901234003', 'Hanoi', TRUE);

INSERT INTO nhan_vien (id, cccd, ho, ten, gioi_tinh, email, sdt, dia_chi, dang_lam_viec) VALUES
('NV001', '986654321001', 'Pham', 'Van D', TRUE, 'nv001@email.com', '0901234004', 'Hanoi', TRUE),
('NV002', '986654321002', 'Hoang', 'Thi E', FALSE, 'nv002@email.com', '0901234005', 'Hanoi', TRUE),
('AD001', '986654321003', 'Nguyen', 'Admin', TRUE, 'ad001@email.com', '0901234006', 'Hanoi', TRUE);

INSERT INTO thiet_bi (ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id, anh) VALUES
('Chìa khóa', 'CO_SAN', 'DI_DONG', 'P101', 'img/key.png'),
('Micro', 'CO_SAN', 'DI_DONG', 'P101', 'img/micro.png'),
('Bút lazer', 'CO_SAN', 'DI_DONG', 'P101', 'img/lazer_pen.png'),
('Sổ đầu bài', 'CO_SAN', 'DI_DONG', 'P101', 'img/so_dau_bai.jpg'),
('Remote máy chiếu', 'CO_SAN', 'DI_DONG', 'P101', 'img/remote.png');

INSERT INTO thiet_bi (ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id, anh) VALUES
('Chìa khóa', 'CO_SAN', 'DI_DONG', 'P102', 'img/key.png'),
('Micro', 'CO_SAN', 'DI_DONG', 'P102', 'img/micro.png'),
('Bút lazer', 'CO_SAN', 'DI_DONG', 'P102', 'img/lazer_pen.png'),
('Sổ đầu bài', 'CO_SAN', 'DI_DONG', 'P102', 'img/so_dau_bai.jpg'),
('Remote máy chiếu', 'CO_SAN', 'DI_DONG', 'P102', 'img/remote.png');

INSERT INTO thiet_bi (ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id, anh) VALUES
('Chìa khóa', 'CO_SAN', 'DI_DONG', 'P201', 'img/key.png'),
('Micro', 'CO_SAN', 'DI_DONG', 'P201', 'img/micro.png'),
('Bút lazer', 'CO_SAN', 'DI_DONG', 'P201', 'img/lazer_pen.png'),
('Sổ đầu bài', 'CO_SAN', 'DI_DONG', 'P201', 'img/so_dau_bai.jpg'),
('Remote máy chiếu', 'CO_SAN', 'DI_DONG', 'P201', 'img/remote.png');

/* CONSTRAINT */

ALTER TABLE phieu_muon
ADD CONSTRAINT chk_ca_gio
CHECK (
    HOUR(ca) IN (6, 12) AND MINUTE(ca) = 0 AND SECOND(ca) = 0
);

/* TRIGGER */

DELIMITER //

CREATE TRIGGER trg_chk_thoi_gian_muon
BEFORE INSERT ON chi_tiet_muon
FOR EACH ROW
BEGIN
    IF NEW.thoi_gian_muon < CURRENT_TIMESTAMP
       OR NEW.thoi_gian_muon > CURRENT_TIMESTAMP + INTERVAL 1 DAY
       OR NOT (
           TIME(NEW.thoi_gian_muon) BETWEEN '06:00:00' AND '10:15:00'
           OR TIME(NEW.thoi_gian_muon) BETWEEN '12:00:00' AND '16:15:00'
       )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Giờ mượn không hợp lệ. Chỉ cho phép từ 06:00–10:15 hoặc 12:00–16:15 trong vòng 1 ngày kể từ hiện tại.';
    END IF;
END //

/* kiem tra hien tai da co phieu muon chua */
CREATE TRIGGER kiem_tra_phieu_muon_hien_tai
BEFORE INSERT 
ON phieu_muon
FOR EACH ROW
BEGIN
    DECLARE so_luong INT;

    SELECT COUNT(*) INTO so_luong
    FROM phieu_muon
    WHERE sinh_vien_id = NEW.sinh_vien_id
      AND DATE(ca) = DATE(NEW.ca)
      AND HOUR(ca) = HOUR(NEW.ca);

    IF so_luong > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Sinh vien da co phieu muon trong cung khung gio nay.';
    END IF;
END //

/* Kiem tra sinh vien da tra het thiet bi truoc do chua */
CREATE TRIGGER kiem_da_tra_het_chua
BEFORE INSERT 
ON phieu_muon
FOR EACH ROW
BEGIN
    DECLARE so_luong INT;

    SELECT COUNT(*) INTO so_luong
    FROM (
        SELECT pm.id AS phieu_muon_id
        FROM phieu_muon pm
        WHERE pm.sinh_vien_id = NEW.sinh_vien_id
          AND pm.ca < NEW.ca
    ) AS pm_filtered
    JOIN (
        SELECT ctm.phieu_muon_id
        FROM chi_tiet_muon ctm
        JOIN thiet_bi tb ON ctm.thiet_bi_id = tb.id
        WHERE ctm.thoi_gian_tra_thuc_te IS NULL
        AND tb.trang_thai NOT IN ('DA_MAT')
    ) AS ctm_filtered
    ON pm_filtered.phieu_muon_id = ctm_filtered.phieu_muon_id
    LIMIT 1;

    IF so_luong > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Sinh viên còn thiết bị chưa trả từ ca trước, không thể mượn mới.';
    END IF;
END //

/* kiem tra phong co duoc muon chua */
CREATE TRIGGER kiem_tra_phong_truoc_them_thiet_bi
BEFORE INSERT ON chi_tiet_muon
FOR EACH ROW
BEGIN
    DECLARE v_phong_id CHAR(5);
    DECLARE v_ca TIMESTAMP;
    DECLARE v_sinh_vien_id VARCHAR(20);
    DECLARE v_conflicting_sinh_vien_id VARCHAR(20);
    DECLARE v_so_luong INT;

    -- Lấy thông tin phiếu mượn hiện tại
    SELECT phong_id, ca, sinh_vien_id
    INTO v_phong_id, v_ca, v_sinh_vien_id
    FROM phieu_muon
    WHERE id = NEW.phieu_muon_id;

    -- Kiểm tra nếu trong cùng ca đã có phiếu duyệt cho phòng này
    SELECT COUNT(*), MAX(sinh_vien_id)
    INTO v_so_luong, v_conflicting_sinh_vien_id
    FROM phieu_muon
    WHERE phong_id = v_phong_id
      AND DATE(ca) = DATE(v_ca)
      AND (
          (TIME(ca) BETWEEN '06:00:00' AND '10:15:00')
          OR
          (TIME(ca) BETWEEN '12:00:00' AND '14:15:00')
      )
      AND trang_thai = 'DA_DUYET'
      AND sinh_vien_id != v_sinh_vien_id;

    IF v_so_luong > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phong da co phieu muon duoc duyet boi sinh vien trong ca này.';
    END IF;
END //

CREATE TRIGGER kiem_tra_phong_truoc_them_phieu_muon
BEFORE INSERT ON phieu_muon
FOR EACH ROW
BEGIN
    DECLARE v_conflicting_sinh_vien_id VARCHAR(20);
    DECLARE v_so_luong INT;

    -- Kiểm tra nếu trong cùng ca đã có phiếu duyệt cho phòng này
    SELECT COUNT(*), MAX(sinh_vien_id)
    INTO v_so_luong, v_conflicting_sinh_vien_id
    FROM phieu_muon
    WHERE phong_id = NEW.phong_id
      AND DATE(ca) = DATE(NEW.ca)
      AND (
          (TIME(ca) BETWEEN '06:00:00' AND '10:15:00')
          OR
          (TIME(ca) BETWEEN '12:00:00' AND '14:15:00')
      )
      AND trang_thai = 'DA_DUYET'
      AND sinh_vien_id != NEW.sinh_vien_id;

    IF v_so_luong > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phong da co phieu muon duoc duyet boi sinh vien trong ca này.';
    END IF;
END //

CREATE TRIGGER kiem_tra_thiet_bi_da_su_dung
BEFORE DELETE
ON thiet_bi
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM chi_tiet_muon WHERE thiet_bi_id = OLD.id LIMIT 1)
       OR EXISTS (SELECT 1 FROM chi_tiet_sua_chua WHERE thiet_bi_id = OLD.id LIMIT 1)
       OR EXISTS (SELECT 1 FROM chi_tiet_thanh_ly WHERE thiet_bi_id = OLD.id LIMIT 1)
       OR EXISTS (SELECT 1 FROM chi_tiet_kiem_ke WHERE thiet_bi_id = OLD.id LIMIT 1) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Thiết bị đã được sử dụng, không thể xóa.';
    END IF;
END //

CREATE TRIGGER kiem_tra_phieu_muon_ca_hien_tai
BEFORE INSERT
ON chi_tiet_muon
FOR EACH ROW
BEGIN
    DECLARE phieu_ca TIMESTAMP;
    SELECT ca INTO phieu_ca
    FROM phieu_muon
    WHERE id = NEW.phieu_muon_id;

    IF NOT (
        DATE(phieu_ca) = CURDATE()
        AND HOUR(phieu_ca) = CASE
            WHEN HOUR(CURRENT_TIME()) BETWEEN 6 AND 10 THEN 6
            WHEN HOUR(CURRENT_TIME()) BETWEEN 12 AND 16 THEN 12
            ELSE -1 
        END
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phiếu mượn không thuộc ca hiện tại.';
    END IF;
END //

CREATE TRIGGER cap_nhat_thoi_gian_tra_khi_hu_hong
AFTER UPDATE
ON thiet_bi
FOR EACH ROW
BEGIN
    IF OLD.trang_thai = 'DANG_MUON' AND NEW.trang_thai = 'HU_HONG' THEN
        UPDATE chi_tiet_muon
        SET thoi_gian_tra_thuc_te = CURRENT_TIMESTAMP
        WHERE thiet_bi_id = NEW.id
          AND thoi_gian_tra_thuc_te IS NULL;
    END IF;
END //

CREATE TRIGGER cap_nhat_trang_thai_thiet_bi_sua_chua
AFTER UPDATE ON phieu_sua_chua
FOR EACH ROW
BEGIN
    -- Nếu trạng thái chuyển sang 'DA_DUYET'
    IF OLD.trang_thai <> 'DA_DUYET' AND NEW.trang_thai = 'DA_DUYET' THEN
        UPDATE thiet_bi
        SET trang_thai = 'DANG_BAO_TRI'
        WHERE id IN (
            SELECT thiet_bi_id
            FROM chi_tiet_sua_chua
            WHERE phieu_sua_chua_id = NEW.id
        );
    END IF;
END //

CREATE TRIGGER cap_nhat_trang_thai_thiet_bi_thanh_ly
AFTER UPDATE ON phieu_thanh_ly
FOR EACH ROW
BEGIN
    -- Chỉ thực hiện khi trạng thái vừa chuyển sang 'DA_DUYET'
    IF OLD.trang_thai <> 'DA_DUYET' AND NEW.trang_thai = 'DA_DUYET' THEN
        UPDATE thiet_bi
        SET trang_thai = 'DA_THANH_LY'
        WHERE id IN (
            SELECT thiet_bi_id
            FROM chi_tiet_thanh_ly
            WHERE phieu_thanh_ly_id = NEW.id
        );
    END IF;
END //

CREATE TRIGGER kiem_tra_tai_khoan_da_hoat_dong
BEFORE DELETE ON tai_khoan
FOR EACH ROW
BEGIN
    DECLARE v_hoat_dong INT DEFAULT 0;

    -- Kiểm tra hoạt động của sinh viên
    IF (EXISTS (
        SELECT 1
        FROM phieu_muon
        WHERE sinh_vien_id = OLD.id
        LIMIT 1
    )) THEN
        SET v_hoat_dong = 1;
    END IF;

    -- Kiểm tra hoạt động của nhân viên
    IF (EXISTS (
        SELECT 1
        FROM phieu_muon
        WHERE nhan_vien_id = OLD.id
        LIMIT 1
    )) THEN
        SET v_hoat_dong = 1;
    END IF;

    -- Chi tiết sửa chữa
    IF (EXISTS (
        SELECT 1
        FROM chi_tiet_sua_chua
        WHERE nhan_vien_id = OLD.id
        LIMIT 1
    )) THEN
        SET v_hoat_dong = 1;
    END IF;

    -- Chi tiết thanh lý
    IF (EXISTS (
        SELECT 1
        FROM chi_tiet_thanh_ly
        WHERE nhan_vien_id = OLD.id
        LIMIT 1
    )) THEN
        SET v_hoat_dong = 1;
    END IF;

    -- Chi tiết kiểm kê
    IF (EXISTS (
        SELECT 1
        FROM chi_tiet_kiem_ke
        WHERE nhan_vien_id = OLD.id
        LIMIT 1
    )) THEN
        SET v_hoat_dong = 1;
    END IF;

    -- Nếu có hoạt động, báo lỗi
    IF v_hoat_dong > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Không thể xoá tài khoản vì đã có hoạt động.';
    END IF;

END //

/* PROCEDURE */

-- 1. lap_phieu_muon
DROP PROCEDURE IF EXISTS lap_phieu_muon;
CREATE PROCEDURE lap_phieu_muon (
    IN p_thiet_bi_ids VARCHAR(255),
    IN p_sinh_vien_id VARCHAR(20)
)
lap_phieu_muon:BEGIN
    DECLARE v_ca TIMESTAMP;
    DECLARE v_thoi_gian_tra_du_kien TIMESTAMP;
    DECLARE v_phong_id CHAR(5);
    DECLARE v_thiet_bi_id INT;
    DECLARE v_pos INT DEFAULT 1;
    DECLARE v_comma_pos INT;
    DECLARE v_thiet_bi_list VARCHAR(255);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    IF HOUR(CURRENT_TIME()) BETWEEN 6 AND 10 THEN
        SET v_ca = CONCAT(CURDATE(), ' 06:00:00');
        SET v_thoi_gian_tra_du_kien = CONCAT(CURDATE(), ' 10:15:00');
    ELSEIF HOUR(CURRENT_TIME()) BETWEEN 12 AND 16 THEN
        SET v_ca = CONCAT(CURDATE(), ' 12:00:00');
        SET v_thoi_gian_tra_du_kien = CONCAT(CURDATE(), ' 16:15:00');
    ELSE
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_SHIFT' AS error_code, 'Thời gian hiện tại không thuộc ca hợp lệ.' AS message;
        LEAVE lap_phieu_muon;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM sinh_vien WHERE id = p_sinh_vien_id AND dang_hoc = TRUE) THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_STUDENT' AS error_code, 'Sinh viên không tồn tại hoặc không đang học.' AS message;
        LEAVE lap_phieu_muon;
    END IF;
    SET v_thiet_bi_list = p_thiet_bi_ids;
    SET v_comma_pos = LOCATE(',', v_thiet_bi_list);
    IF v_comma_pos = 0 THEN
        SET v_thiet_bi_id = CAST(v_thiet_bi_list AS UNSIGNED);
    ELSE
        SET v_thiet_bi_id = CAST(SUBSTRING(v_thiet_bi_list, 1, v_comma_pos - 1) AS UNSIGNED);
    END IF;
    SELECT phong_id INTO v_phong_id FROM thiet_bi WHERE id = v_thiet_bi_id;
    IF v_phong_id IS NULL THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_EQUIPMENT' AS error_code, 'Thiết bị đầu tiên không tồn tại.' AS message;
        LEAVE lap_phieu_muon;
    END IF;
    SET v_thiet_bi_list = CONCAT(p_thiet_bi_ids, ',');
    SET v_pos = 1;
    WHILE v_pos < LENGTH(v_thiet_bi_list) DO
        SET v_comma_pos = LOCATE(',', v_thiet_bi_list, v_pos);
        SET v_thiet_bi_id = CAST(SUBSTRING(v_thiet_bi_list, v_pos, v_comma_pos - v_pos) AS UNSIGNED);
        SET v_pos = v_comma_pos + 1;
        IF NOT EXISTS (
            SELECT 1 FROM thiet_bi WHERE id = v_thiet_bi_id AND trang_thai = 'CO_SAN' AND phong_id = v_phong_id
        ) THEN
            ROLLBACK;
            SELECT 0 AS success, 'INVALID_EQUIPMENT', CONCAT('Thiết bị ID ', v_thiet_bi_id, ' không tồn tại, không sẵn sàng, hoặc không thuộc phòng ', v_phong_id) AS message;
            LEAVE lap_phieu_muon;
        END IF;
    END WHILE;
    INSERT INTO phieu_muon (sinh_vien_id, nhan_vien_id, phong_id, ca, thoi_gian_tra_du_kien)
    VALUES (p_sinh_vien_id, NULL, v_phong_id, v_ca, v_thoi_gian_tra_du_kien);
    SET @p_phieu_muon_id = LAST_INSERT_ID();
    SET v_thiet_bi_list = CONCAT(p_thiet_bi_ids, ',');
    SET v_pos = 1;
    WHILE v_pos < LENGTH(v_thiet_bi_list) DO
        SET v_comma_pos = LOCATE(',', v_thiet_bi_list, v_pos);
        SET v_thiet_bi_id = CAST(SUBSTRING(v_thiet_bi_list, v_pos, v_comma_pos - v_pos) AS UNSIGNED);
        SET v_pos = v_comma_pos + 1;
        INSERT INTO chi_tiet_muon (phieu_muon_id, thiet_bi_id, thoi_gian_muon, thoi_gian_tra_thuc_te)
        VALUES (@p_phieu_muon_id, v_thiet_bi_id, CURRENT_TIMESTAMP, NULL);
    END WHILE;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- 2. xac_nhan_phieu_muon
DROP PROCEDURE IF EXISTS xac_nhan_phieu_muon;
CREATE PROCEDURE xac_nhan_phieu_muon (
    IN p_phieu_muon_id INT,
    IN p_nhan_vien_id VARCHAR(20)
)
xac_nhan_phieu_muon:BEGIN
    DECLARE v_so_luong INT;
    DECLARE v_phong_id CHAR(5);
    DECLARE v_ca TIMESTAMP;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    IF NOT EXISTS (SELECT 1 FROM phieu_muon WHERE id = p_phieu_muon_id) THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_BORROW', 'Phiếu mượn không tồn tại.' AS message;
        LEAVE xac_nhan_phieu_muon;
    END IF;
    SELECT phong_id, ca INTO v_phong_id, v_ca FROM phieu_muon WHERE id = p_phieu_muon_id;
    SELECT COUNT(*) INTO v_so_luong
    FROM chi_tiet_muon ctm
    JOIN thiet_bi tb ON ctm.thiet_bi_id = tb.id
    WHERE ctm.phieu_muon_id = p_phieu_muon_id
      AND tb.trang_thai = 'CO_SAN';
    IF v_so_luong = 0 THEN
        ROLLBACK;
        SELECT 0 AS success, 'NO_AVAILABLE_EQUIPMENT', 'Không có thiết bị nào sẵn sàng để duyệt.' AS message;
        LEAVE xac_nhan_phieu_muon;
    END IF;
    UPDATE thiet_bi tb
    JOIN chi_tiet_muon ctm ON tb.id = ctm.thiet_bi_id
    SET tb.trang_thai = 'DANG_MUON'
    WHERE ctm.phieu_muon_id = p_phieu_muon_id
      AND tb.trang_thai = 'CO_SAN';

    UPDATE phieu_muon SET trang_thai = 'DA_DUYET', nhan_vien_id = p_nhan_vien_id
    WHERE id = p_phieu_muon_id;

    -- Xóa các phiếu mượn chưa được duyệt cùng phòng, cùng ca, khác sinh viên
    DELETE FROM phieu_muon
    WHERE id <> p_phieu_muon_id
      AND phong_id = v_phong_id
      AND ca = v_ca
      AND trang_thai = 'CHO_DUYET';
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- Thêm event tự động xóa các phiếu mượn chưa được duyệt khi hết ca
CREATE EVENT IF NOT EXISTS ev_delete_expired_borrow_requests
ON SCHEDULE EVERY 5 MINUTE
DO
  DELETE FROM phieu_muon
  WHERE trang_thai = 'CHO_DUYET'
    AND (
      (HOUR(ca) = 6 AND NOW() > CONCAT(DATE(ca), ' 10:15:00'))
      OR
      (HOUR(ca) = 12 AND NOW() > CONCAT(DATE(ca), ' 16:15:00'))
    );

-- 3. them_thiet_bi_vao_phieu_muon
CREATE PROCEDURE them_thiet_bi_vao_phieu_muon (
    IN p_phieu_muon_id INT,
    IN p_thiet_bi_ids VARCHAR(255)
)
them_thiet_bi_vao_phieu_muon:BEGIN
    DECLARE v_phong_id CHAR(5);
    DECLARE v_ca TIMESTAMP;
    DECLARE v_thiet_bi_id INT;
    DECLARE v_pos INT DEFAULT 1;
    DECLARE v_comma_pos INT;
    DECLARE v_thiet_bi_list VARCHAR(255);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    SELECT phong_id,ca INTO v_phong_id, v_ca FROM phieu_muon WHERE id = p_phieu_muon_id;
    IF v_phong_id IS NULL THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_BORROW', 'Phiếu mượn không tồn tại.' AS message;
        LEAVE them_thiet_bi_vao_phieu_muon;
    END IF;
    IF NOT (
        DATE(v_ca) = CURDATE()
        AND HOUR(v_ca) = CASE
            WHEN HOUR(CURRENT_TIME()) BETWEEN 6 AND 10 THEN 6
            WHEN HOUR(CURRENT_TIME()) BETWEEN 12 AND 16 THEN 12
            ELSE -1
        END
    ) THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_SHIFT', 'Phiếu mượn không thuộc ca hiện tại.' AS message;
        LEAVE them_thiet_bi_vao_phieu_muon;
    END IF;
    SET v_thiet_bi_list = CONCAT(p_thiet_bi_ids, ',');
    SET v_pos = 1;
    WHILE v_pos < LENGTH(v_thiet_bi_list) DO
        SET v_comma_pos = LOCATE(',', v_thiet_bi_list, v_pos);
        SET v_thiet_bi_id = CAST(SUBSTRING(v_thiet_bi_list, v_pos, v_comma_pos - v_pos) AS UNSIGNED);
        SET v_pos = v_comma_pos + 1;
        IF NOT EXISTS (
            SELECT 1 FROM thiet_bi WHERE id = v_thiet_bi_id AND trang_thai = 'CO_SAN' AND phong_id = v_phong_id
        ) THEN
            ROLLBACK;
            SELECT 0 AS success, 'INVALID_EQUIPMENT', CONCAT('Thiết bị ID ', v_thiet_bi_id, ' không tồn tại, không sẵn sàng, hoặc không thuộc phòng ', v_phong_id) AS message;
            LEAVE them_thiet_bi_vao_phieu_muon;
        END IF;
        IF EXISTS (
            SELECT 1 FROM chi_tiet_muon WHERE phieu_muon_id = p_phieu_muon_id AND thiet_bi_id = v_thiet_bi_id
        ) THEN
            ROLLBACK;
            SELECT 0 AS success, 'DUPLICATE_EQUIPMENT', CONCAT('Thiết bị ID ', v_thiet_bi_id, ' đã có trong phiếu mượn này.') AS message;
            LEAVE them_thiet_bi_vao_phieu_muon;
        END IF;
        INSERT INTO chi_tiet_muon (phieu_muon_id, thiet_bi_id, thoi_gian_muon, thoi_gian_tra_thuc_te)
        VALUES (p_phieu_muon_id, v_thiet_bi_id, CURRENT_TIMESTAMP, NULL);
    END WHILE;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- 4. cap_nhat_thong_tin_thiet_bi
DROP PROCEDURE IF EXISTS cap_nhat_thong_tin_thiet_bi;
CREATE PROCEDURE cap_nhat_thong_tin_thiet_bi (
    IN p_id INT,
    IN p_ten_thiet_bi VARCHAR(100),
    IN p_trang_thai ENUM('CO_SAN', 'DANG_BAO_TRI', 'DANG_MUON', 'HU_HONG', 'DA_THANH_LY', 'DA_MAT'),
    IN p_loai_thiet_bi ENUM('DI_DONG', 'CO_DINH'),
    IN p_phong_id CHAR(5)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    IF NOT EXISTS (SELECT 1 FROM thiet_bi WHERE id = p_id) THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_EQUIPMENT', 'Thiết bị không tồn tại!' AS message;
    ELSE
        UPDATE thiet_bi
        SET
            ten_thiet_bi = p_ten_thiet_bi,
            trang_thai = p_trang_thai,
            loai_thiet_bi = p_loai_thiet_bi,
            phong_id = p_phong_id
        WHERE id = p_id;
        COMMIT;
        SELECT 1 AS success, NULL AS error_code, NULL AS message;
    END IF;
END //

-- 5. them_thiet_bi_moi
DROP PROCEDURE IF EXISTS them_thiet_bi_moi;
CREATE PROCEDURE them_thiet_bi_moi (
    IN p_ten_thiet_bi VARCHAR(100),
    IN p_trang_thai ENUM('CO_SAN', 'DANG_BAO_TRI', 'DANG_MUON', 'HU_HONG', 'DA_THANH_LY', 'DA_MAT'),
    IN p_loai_thiet_bi ENUM('DI_DONG', 'CO_DINH'),
    IN p_phong_id CHAR(5)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    IF NOT EXISTS (SELECT 1 FROM phong WHERE id = p_phong_id) THEN
        ROLLBACK;
        SELECT 0 AS success, 'INVALID_ROOM', 'Phòng không tồn tại!' AS message;
    ELSE
        INSERT INTO thiet_bi (
            ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id
        )
        VALUES (
            p_ten_thiet_bi, p_trang_thai, p_loai_thiet_bi, p_phong_id
        );
        COMMIT;
        SELECT 1 AS success, NULL AS error_code, NULL AS message;
    END IF;
END //

-- 6. them_thiet_bi_sua_chua
DROP PROCEDURE IF EXISTS them_thiet_bi_sua_chua;
CREATE PROCEDURE them_thiet_bi_sua_chua (
    IN p_nhan_vien_id VARCHAR(20),
    IN p_thiet_bi_id INT,
    IN p_gia DOUBLE,
    IN p_ghi_chu TEXT
)
BEGIN
    DECLARE v_phieu_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    SELECT id INTO v_phieu_id
    FROM phieu_sua_chua
    WHERE nhan_vien_id = p_nhan_vien_id AND trang_thai = 'CHUAN_BI'
    LIMIT 1;
    IF v_phieu_id IS NULL THEN
        INSERT INTO phieu_sua_chua (ngay_bat_dau, trang_thai, nhan_vien_id)
        VALUES (NOW(), 'CHUAN_BI', p_nhan_vien_id);
        SET v_phieu_id = LAST_INSERT_ID();
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM chi_tiet_sua_chua
        WHERE phieu_sua_chua_id = v_phieu_id AND thiet_bi_id = p_thiet_bi_id
    ) THEN
        INSERT INTO chi_tiet_sua_chua (phieu_sua_chua_id, thiet_bi_id, gia, ghi_chu)
        VALUES (v_phieu_id, p_thiet_bi_id, p_gia, p_ghi_chu);
    END IF;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- 7. them_thiet_bi_thanh_ly
DROP PROCEDURE IF EXISTS them_thiet_bi_thanh_ly;
CREATE PROCEDURE them_thiet_bi_thanh_ly (
    IN p_nhan_vien_id VARCHAR(20),
    IN p_thiet_bi_id INT,
    IN p_gia DOUBLE,
    IN p_ghi_chu TEXT
)
BEGIN
    DECLARE v_phieu_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    SELECT id INTO v_phieu_id
    FROM phieu_thanh_ly
    WHERE nhan_vien_id = p_nhan_vien_id AND trang_thai = 'CHUAN_BI'
    LIMIT 1;
    IF v_phieu_id IS NULL THEN
        INSERT INTO phieu_thanh_ly (ngay_thanh_ly, trang_thai, nhan_vien_id)
        VALUES (NOW(), 'CHUAN_BI', p_nhan_vien_id);
        SET v_phieu_id = LAST_INSERT_ID();
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM chi_tiet_thanh_ly
        WHERE phieu_thanh_ly_id = v_phieu_id AND thiet_bi_id = p_thiet_bi_id
    ) THEN
        INSERT INTO chi_tiet_thanh_ly (phieu_thanh_ly_id, thiet_bi_id, gia, ghi_chu)
        VALUES (v_phieu_id, p_thiet_bi_id, p_gia, p_ghi_chu);
    END IF;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- 8. tao_tai_khoan_moi
DROP PROCEDURE IF EXISTS tao_tai_khoan_moi;
CREATE PROCEDURE tao_tai_khoan_moi (
    IN p_id VARCHAR(20),
    IN p_mat_khau VARCHAR(500),
    IN p_ten_vai_tro VARCHAR(100),
    IN p_cccd CHAR(12),
    IN p_ho VARCHAR(50),
    IN p_ten VARCHAR(50),
    IN p_gioi_tinh BOOLEAN,
    IN p_email VARCHAR(100),
    IN p_sdt CHAR(10),
    IN p_dia_chi VARCHAR(255),
    IN p_lop_id VARCHAR(20)
)
BEGIN
    DECLARE v_vai_tro_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    SELECT id INTO v_vai_tro_id FROM vai_tro WHERE ten_vai_tro = p_ten_vai_tro;
    INSERT INTO tai_khoan (id, mat_khau, vai_tro_id)
    VALUES (p_id, p_mat_khau, v_vai_tro_id);
    IF p_ten_vai_tro = 'sinh_vien' THEN
        INSERT INTO sinh_vien (id, lop_id, cccd, ho, ten, gioi_tinh, email, sdt, dia_chi)
        VALUES (p_id, p_lop_id, p_cccd, p_ho, p_ten, p_gioi_tinh, p_email, p_sdt, p_dia_chi);
    ELSEIF p_ten_vai_tro = 'nhan_vien' OR p_ten_vai_tro = 'quan_ly' THEN
        INSERT INTO nhan_vien (id, cccd, ho, ten, gioi_tinh, email, sdt, dia_chi)
        VALUES (p_id, p_cccd, p_ho, p_ten, p_gioi_tinh, p_email, p_sdt, p_dia_chi);
    END IF;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

-- 9. cap_nhat_tai_khoan
DROP PROCEDURE IF EXISTS cap_nhat_tai_khoan;
CREATE PROCEDURE cap_nhat_tai_khoan (
    IN p_id VARCHAR(20),
    IN p_mat_khau VARCHAR(500),
    IN p_dang_hoat_dong BOOLEAN,
    IN p_cccd CHAR(12),
    IN p_ho VARCHAR(50),
    IN p_ten VARCHAR(50),
    IN p_gioi_tinh BOOLEAN,
    IN p_email VARCHAR(100),
    IN p_sdt CHAR(10),
    IN p_dia_chi VARCHAR(255),
    IN p_lop_id VARCHAR(20)
)
BEGIN
    DECLARE v_ten_vai_tro VARCHAR(100);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 0 AS success, 'SQL_EXCEPTION' AS error_code, 'Lỗi hệ thống hoặc truy vấn.' AS message;
    END;
    START TRANSACTION;
    SELECT ten_vai_tro INTO v_ten_vai_tro
    FROM tai_khoan tk
    JOIN vai_tro vt ON tk.vai_tro_id = vt.id
    WHERE tk.id = p_id;
    UPDATE tai_khoan
    SET mat_khau = p_mat_khau,
        dang_hoat_dong = p_dang_hoat_dong
    WHERE id = p_id;
    IF v_ten_vai_tro = 'sinh_vien' THEN
        UPDATE sinh_vien
        SET lop_id = p_lop_id,
            cccd = p_cccd,
            ho = p_ho,
            ten = p_ten,
            gioi_tinh = p_gioi_tinh,
            email = p_email,
            sdt = p_sdt,
            dia_chi = p_dia_chi
        WHERE id = p_id;
    ELSE
        UPDATE nhan_vien
        SET cccd = p_cccd,
            ho = p_ho,
            ten = p_ten,
            gioi_tinh = p_gioi_tinh,
            email = p_email,
            sdt = p_sdt,
            dia_chi = p_dia_chi
        WHERE id = p_id;
    END IF;
    COMMIT;
    SELECT 1 AS success, NULL AS error_code, NULL AS message;
END //

CREATE PROCEDURE them_chi_tiet_kiem_ke (
    IN p_phieu_kiem_ke_id INT,
    IN p_phong_id CHAR(5),
    IN p_tong_so INT,
    IN p_ghi_chu VARCHAR(255),
    IN p_so_luong_hong INT,
    IN p_so_luong_sua_chua INT,
    IN p_so_luong_thanh_ly INT
)
BEGIN
    -- Kiểm tra phiếu kiểm kê có tồn tại không
    IF NOT EXISTS (
        SELECT 1 FROM phieu_kiem_ke WHERE id = p_phieu_kiem_ke_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phieu kiem ke khong ton tai.';
    END IF;

    -- Kiểm tra tổng hợp hợp lệ
    IF p_tong_so < 0
        OR p_so_luong_hong < 0
        OR p_so_luong_sua_chua < 0
        OR p_so_luong_thanh_ly < 0
        OR (p_so_luong_hong + p_so_luong_sua_chua + p_so_luong_thanh_ly > p_tong_so)
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Du lieu so luong khong hop le.';
    END IF;

    -- Thêm chi tiết kiểm kê
    INSERT INTO chi_tiet_kiem_ke (
        phieu_kiem_ke_id,
        phong_id,
        tong_so,
        ghi_chu,
        so_luong_hong,
        so_luong_sua_chua,
        so_luong_thanh_ly
    ) VALUES (
        p_phieu_kiem_ke_id,
        p_phong_id,
        p_tong_so,
        p_ghi_chu,
        p_so_luong_hong,
        p_so_luong_sua_chua,
        p_so_luong_thanh_ly
    );
END //

CREATE PROCEDURE duyet_mot_thiet_bi(IN p_thiet_bi_id INT)
BEGIN
    DECLARE p_phieu_muon_id INT;

    -- Tìm phiếu mượn chứa thiết bị trong khoảng thời gian quy định hôm nay
    SELECT ctm.phieu_muon_id
    INTO p_phieu_muon_id
    FROM chi_tiet_muon ctm
    JOIN phieu_muon pm ON ctm.phieu_muon_id = pm.id
    WHERE ctm.thiet_bi_id = p_thiet_bi_id
      AND DATE(pm.ca) = CURDATE()
      AND (
        TIME(pm.ca) BETWEEN '06:00:00' AND '10:15:00'
        OR TIME(pm.ca) BETWEEN '12:00:00' AND '16:15:00'
      )
    LIMIT 1;

    -- Nếu có phiếu mượn
    IF p_phieu_muon_id IS NOT NULL THEN
        -- Cập nhật trạng thái thiết bị
        UPDATE thiet_bi
        SET trang_thai = 'DANG_MUON'
        WHERE id = p_thiet_bi_id;

        -- Cập nhật trạng thái phiếu mượn
        UPDATE phieu_muon
        SET trang_thai = 'DA_DUYET'
        WHERE id = p_phieu_muon_id;
    END IF;
END;

CREATE PROCEDURE tu_choi_mot_thiet_bi(IN p_thiet_bi_id INT)
BEGIN
    DELETE ctm
    FROM chi_tiet_muon ctm
    JOIN phieu_muon pm ON ctm.phieu_muon_id = pm.id
    WHERE ctm.thiet_bi_id = p_thiet_bi_id
      AND DATE(pm.ca) = CURDATE()
      AND (
        TIME(pm.ca) BETWEEN '06:00:00' AND '10:15:00'
        OR TIME(pm.ca) BETWEEN '12:00:00' AND '16:15:00'
      );
END;
//

DELIMITER ;

