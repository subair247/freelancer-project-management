CREATE DATABASE IF NOT EXISTS freelancing_db;
USE freelancing_db;

-- Module 1: User & Profile Management Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Module 2: Client & Lead Operations Table
CREATE TABLE IF NOT EXISTS clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    client_name VARCHAR(100) NOT NULL,
    company_name VARCHAR(100),
    contact_email VARCHAR(100),
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Module 3: Project Execution & Workflow Table
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    project_name VARCHAR(150) NOT NULL,
    milestones TEXT,
    deadline DATE,
    project_status VARCHAR(50),
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

-- Module 4: Performance & Analytics Table
CREATE TABLE IF NOT EXISTS performance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    income_generated DECIMAL(10, 2),
    feedback_score INT,
    improvisation_notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);