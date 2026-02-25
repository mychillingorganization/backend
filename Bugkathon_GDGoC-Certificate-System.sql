CREATE DATABASE GDGoCCertificateSystemDb;
GO
USE GDGoCCertificateSystemDb;
GO

-- 2. Tạo bảng users (Core Team)
CREATE TABLE users (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NULL,
    name NVARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 3. Tạo bảng events (Sự kiện)
CREATE TABLE events (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    name NVARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    created_by UNIQUEIDENTIFIER NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Events_Users FOREIGN KEY (created_by) REFERENCES users(id)
);
GO

-- 4. Tạo bảng templates (Mẫu SVG)
CREATE TABLE templates (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    event_id UNIQUEIDENTIFIER NOT NULL,
    name NVARCHAR(255) NOT NULL,
    svg_content NVARCHAR(MAX) NOT NULL, -- Sử dụng NVARCHAR(MAX) để lưu chuỗi XML/SVG không giới hạn độ dài
    variables NVARCHAR(MAX) NOT NULL, -- SQL Server lưu JSON dưới dạng chuỗi text
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Templates_Events FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
GO

-- 5. Tạo bảng generation_log (Tiến trình xử lý hàng loạt)
CREATE TABLE generation_log (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    template_id UNIQUEIDENTIFIER NOT NULL,
    google_sheet_url NVARCHAR(MAX) NOT NULL,
    drive_folder_id VARCHAR(255) NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- PENDING, PROCESSING, COMPLETED, FAILED
    total_records INT NOT NULL DEFAULT 0,
    processed INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_GenerationLog_Templates FOREIGN KEY (template_id) REFERENCES templates(id)
);
GO

-- 6. Tạo bảng generated_assets (Ấn phẩm chi tiết)
CREATE TABLE generated_assets (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    generation_log_id UNIQUEIDENTIFIER NOT NULL,
    participant_name NVARCHAR(255) NOT NULL,
    participant_email VARCHAR(255) NOT NULL,
    drive_file_id VARCHAR(255) NULL,
    email_status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- PENDING, SENT, FAILED
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_GeneratedAssets_GenerationLog FOREIGN KEY (generation_log_id) REFERENCES generation_log(id) ON DELETE CASCADE
);
GO