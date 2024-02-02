-- Create the database and switch to it
CREATE DATABASE IF NOT EXISTS school;
USE school;

-- Create necessary users and grant privileges
CREATE USER IF NOT EXISTS 'QBE'@'%' IDENTIFIED WITH mysql_native_password BY 'qbe';
GRANT ALL PRIVILEGES ON school.* TO 'QBE'@'%';
FLUSH PRIVILEGES;


USE school;

-- Create the 'Classrooms' table
CREATE TABLE IF NOT EXISTS Classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(50),
    capacity INT
);

-- Create the 'Students' table
CREATE TABLE IF NOT EXISTS Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    grade_level INT,
    classroom_id INT,
    FOREIGN KEY (classroom_id) REFERENCES Classrooms (id)
);

-- Create the 'Teachers' table
CREATE TABLE IF NOT EXISTS Teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE
);

-- Create the 'Subjects' table
CREATE TABLE IF NOT EXISTS Subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- Create the 'Courses' table
CREATE TABLE IF NOT EXISTS Courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    teacher_id INT,
    subject_id INT,
    FOREIGN KEY (teacher_id) REFERENCES Teachers (id),
    FOREIGN KEY (subject_id) REFERENCES Subjects (id)
);

-- Create the 'Grades' table
CREATE TABLE IF NOT EXISTS Grades (
    student_id INT,
    course_id INT,
    grade VARCHAR(100),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students (id),
    FOREIGN KEY (course_id) REFERENCES Courses (id)
);

-- Create the 'Attendance' table
CREATE TABLE IF NOT EXISTS Attendance (
    student_id INT,
    date DATE,
    status VARCHAR(10),
    PRIMARY KEY (student_id, date),
    FOREIGN KEY (student_id) REFERENCES Students (id)
);

-- Create the 'SchoolEvents' table
CREATE TABLE IF NOT EXISTS SchoolEvents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    event_date DATE,
    description TEXT
);

-- Create the 'ParentGuardian' table
CREATE TABLE IF NOT EXISTS ParentGuardian (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    name VARCHAR(100),
    relationship VARCHAR(50),
    contact_info VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES Students (id)
);


-- Inserting data into 'Classrooms'
INSERT INTO Classrooms (room_number, capacity) VALUES
('101', 30),
('102', 28),
('103', 25),
('104', 20),
('105', 30),
('106', 32),
('107', 28),
('108', 35),
('109', 22),
('110', 30),
('111', 24),
('112', 34);

-- Inserting data into 'Students'
INSERT INTO Students (name, grade_level, classroom_id) VALUES
('John Doe', 10, 1),
('Jane Smith', 11, 2),
('Emily Johnson', 10, 1),
('Alice Johnson', 9, 3),
('Brian Lee', 10, 4),
('Charlie Brown', 12, 5),
('Diana Prince', 11, 6),
('Ethan Hunt', 9, 7),
('Fiona Gallagher', 10, 8),
('George Weasley', 12, 9),
('Hermione Granger', 11, 10),
('Ian Malcolm', 9, 11),
('Julia Styles', 10, 12);

-- Inserting data into 'Teachers'
INSERT INTO Teachers (name, hire_date) VALUES
('Mr. Anderson', '2015-08-20'),
('Ms. Brown', '2018-09-15'),
('Ms. Carter', '2020-01-10'),
('Mr. Watson', '2019-03-20'),
('Mrs. Lopez', '2016-07-15'),
('Dr. Adams', '2017-08-30'),
('Prof. Morris', '2014-11-25'),
('Ms. O’Neil', '2021-02-14'),
('Mr. Davidson', '2018-05-22'),
('Mrs. Chang', '2015-09-18'),
('Dr. Baker', '2022-01-07'),
('Prof. Allen', '2020-06-05');

-- Inserting data into 'Subjects'
INSERT INTO Subjects (name) VALUES
('Mathematics'),
('Science'),
('History'),
('Geography'),
('Physics'),
('Chemistry'),
('English'),
('Art'),
('Music'),
('Physical Education'),
('Biology'),
('Computer Science'),
('Economics');

-- Inserting data into 'Courses'
INSERT INTO Courses (name, teacher_id, subject_id) VALUES
('Algebra', 1, 1),
('Biology', 2, 2),
('World History', 2, 3),
('Geography 101', 4, 6),
('Physics 201', 5, 7),
('Chemistry 301', 6, 8),
('English Literature', 7, 9),
('Art History', 8, 10),
('Music Theory', 9, 11),
('Gym', 10, 12),
('Biology 102', 3, 13);

-- Inserting data into 'Grades'
INSERT INTO Grades (student_id, course_id, grade) VALUES
(1, 1, 'A'),
(2, 2, 'B'),
(3, 3, 'A'),
(4, 4, 'B'),
(5, 5, 'C'),
(6, 6, 'B'),
(7, 7, 'A'),
(8, 8, 'A'),
(9, 9, 'C'),
(10, 10, 'B'),
(11, 11, 'A');

-- Inserting data into 'Attendance'
INSERT INTO Attendance (student_id, date, status) VALUES
(1, '2024-01-10', 'Present'),
(2, '2024-01-10', 'Absent'),
(3, '2024-01-10', 'Present'),
(4, '2024-01-11', 'Present'),
(5, '2024-01-11', 'Absent'),
(6, '2024-01-11', 'Present'),
(7, '2024-01-11', 'Absent'),
(8, '2024-01-11', 'Present'),
(9, '2024-01-11', 'Absent'),
(10, '2024-01-11', 'Present'),
(11, '2024-01-11', 'Absent'),
(12, '2024-01-11', 'Present'),
(13, '2024-01-11', 'Absent');

-- Inserting data into 'SchoolEvents'
INSERT INTO SchoolEvents (title, event_date, description) VALUES
('Science Fair', '2024-05-15', 'Annual school science fair.'),
('Math Competition', '2024-04-10', 'Annual math competition.'),
('Art Show', '2024-06-15', 'Exhibition of student artwork.'),
('Spring Concert', '2024-03-20', 'Performance by the school band and choir.'),
('Career Day', '2024-05-25', 'Professionals talk about their careers.'),
('Book Fair', '2024-10-05', 'Sale of books and literary discussions.'),
('Sports Day', '2024-09-12', 'Various sports competitions.'),
('Science Exhibition', '2024-11-15', 'Display of science projects.'),
('Theater Play', '2024-07-20', 'Drama club presents a play.'),
('Dance Night', '2024-08-30', 'School dance for students.'),
('Fundraiser', '2024-12-10', 'Event to raise funds for school activities.');

-- Inserting data into 'ParentGuardian'
INSERT INTO ParentGuardian (student_id, name, relationship, contact_info) VALUES
(1, 'David Doe', 'Father', 'david.doe@email.com'),
(2, 'Sarah Smith', 'Mother', 'sarah.smith@email.com'),
(3, 'Lisa Johnson', 'Mother', 'lisa.johnson@email.com'),
(4, 'Michael Lee', 'Father', 'michael.lee@email.com'),
(5, 'Nancy Brown', 'Mother', 'nancy.brown@email.com'),
(6, 'Peter Prince', 'Father', 'peter.prince@email.com'),
(7, 'Susan Hunt', 'Mother', 'susan.hunt@email.com'),
(8, 'Frank Gallagher', 'Father', 'frank.gallagher@email.com'),
(9, 'Molly Weasley', 'Mother', 'molly.weasley@email.com'),
(10, 'Arthur Granger', 'Father', 'arthur.granger@email.com'),
(11, 'Emma Malcolm', 'Mother', 'emma.malcolm@email.com'),
(12, 'Oliver Styles', 'Father', 'oliver.styles@email.com'),
(13, 'Destiny Ranger', 'Mother', 'destiny.ranger@email.com');
