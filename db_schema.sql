-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'university_supervisor', 'pending_supervisor', 'industry_supervisor', 'coordinator', 'cod', 'admin') NOT NULL,
    status ENUM('active', 'pending', 'inactive') DEFAULT 'pending',
    student_level ENUM('diploma', 'degree', NULL) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RETURN FORMS
CREATE TABLE return_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    supervisor_name VARCHAR(100) NOT NULL,
    supervisor_email VARCHAR(100) NOT NULL,
    supervisor_phone VARCHAR(20),
    insurance_form VARCHAR(255), -- file path
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- LOGBOOKS
CREATE TABLE logbooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    week INT NOT NULL,
    entry TEXT NOT NULL,
    verified_by INT, -- supervisor id
    verified_on TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

-- FINAL REPORTS
CREATE TABLE final_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    report_file VARCHAR(255) NOT NULL,
    logbook_file VARCHAR(255) NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- ASSESSMENTS
CREATE TABLE assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    university_score INT,
    industry_score INT,
    comments TEXT,
    assessed_by INT, -- supervisor id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (assessed_by) REFERENCES users(id)
);

-- SUPERVISORS (for mapping students to supervisors)
CREATE TABLE supervisors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    university_supervisor_id INT,
    industry_supervisor_id INT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (university_supervisor_id) REFERENCES users(id),
    FOREIGN KEY (industry_supervisor_id) REFERENCES users(id)
);

-- NOTIFICATIONS
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- DEFER/CHANGE PLACEMENT REQUESTS
CREATE TABLE placement_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    type ENUM('deferral', 'change') NOT NULL,
    reason TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- CLUSTERS/ZONES
CREATE TABLE clusters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    coordinator_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coordinator_id) REFERENCES users(id)
);

-- STUDENT-CLUSTER ASSIGNMENT
CREATE TABLE student_clusters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    cluster_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (cluster_id) REFERENCES clusters(id)
); 