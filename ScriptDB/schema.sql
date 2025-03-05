-- filepath: /d:/Proyectos/Analizador/src/core/database/schema.sql
-- Users and Authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user', 'api') NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Add user preferences and API keys
CREATE TABLE user_settings (
    user_id INT PRIMARY KEY,
    preferences JSON,
    api_keys JSON,
    notification_settings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Files and Documents
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    filename VARCHAR(1024) NOT NULL COMMENT 'Ruta completa al archivo original',
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    file_metadata JSON,  -- Cambiado de metadata a file_metadata
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add file relationships table
CREATE TABLE file_relationships (
    source_file_id INT,
    related_file_id INT,
    relationship_type VARCHAR(50),
    confidence FLOAT,
    relationship_metadata JSON,  -- Cambiado de metadata a relationship_metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_file_id, related_file_id),
    FOREIGN KEY (source_file_id) REFERENCES files(id),
    FOREIGN KEY (related_file_id) REFERENCES files(id)
);

-- Categories and Tags
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(1000),  -- Cambiado de TEXT a VARCHAR(1000)
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- File Categories Relation
CREATE TABLE file_categories (
    file_id INT,
    category_id INT,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (file_id, category_id),
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Processing Queue
CREATE TABLE processing_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    priority INT DEFAULT 0,
    attempts INT DEFAULT 0,
    error_message VARCHAR(1000),  -- Cambiado de TEXT a VARCHAR(1000)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    parent_task_id INT,
    task_type VARCHAR(50) NOT NULL DEFAULT 'file_processing',
    timeout_seconds INT DEFAULT 3600,
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (parent_task_id) REFERENCES processing_queue(id)
);

-- AI Analysis Results
CREATE TABLE analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    analysis_type VARCHAR(50) NOT NULL,
    confidence FLOAT,
    result_data JSON,
    language VARCHAR(10),
    summary TEXT,
    keywords JSON,
    extracted_metadata JSON,
    content_hash VARCHAR(64),
    processing_metadata JSON,
    model_used VARCHAR(100),
    tokens_used INT,
    processing_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Plugins Registry
CREATE TABLE plugins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    version VARCHAR(20) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    settings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP
);

-- File Processing History
CREATE TABLE processing_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    plugin_id INT,
    status ENUM('success', 'failure') NOT NULL,
    processing_time FLOAT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (plugin_id) REFERENCES plugins(id)
);

-- System Logs
CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    component VARCHAR(50),
    message VARCHAR(2000),       -- Cambiado de TEXT a VARCHAR(2000)
    stack_trace VARCHAR(4000),   -- Cambiado de TEXT a VARCHAR(4000)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Metrics
CREATE TABLE performance_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(50) NOT NULL,
    metric_value FLOAT NOT NULL,
    component VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add entity extraction table
CREATE TABLE extracted_entities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    entity_type VARCHAR(50),
    entity_value VARCHAR(1000),  -- Cambiado de TEXT a VARCHAR(1000)
    confidence FLOAT,
    context VARCHAR(2000),       -- Cambiado de TEXT a VARCHAR(2000)
    entity_metadata JSON,  -- Cambiado de metadata a entity_metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Add tasks and scheduling
CREATE TABLE scheduled_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_type VARCHAR(50),
    schedule_type ENUM('one-time', 'recurring'),
    cron_expression VARCHAR(100),
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    settings JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add API usage tracking
CREATE TABLE api_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    response_time FLOAT,
    status_code INT,
    request_size INT,
    response_size INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX idx_files_type ON files(file_type);
CREATE INDEX idx_files_processed ON files(is_processed);
CREATE INDEX idx_queue_status ON processing_queue(status);
CREATE INDEX idx_analysis_file ON analysis_results(file_id);
CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_logs_component ON system_logs(component);
CREATE INDEX idx_metrics_name ON performance_metrics(metric_name);

-- Add indexes for new tables
CREATE INDEX idx_entity_type ON extracted_entities(entity_type);
CREATE INDEX idx_entity_file ON extracted_entities(file_id);
CREATE INDEX idx_task_next_run ON scheduled_tasks(next_run, is_active);
CREATE INDEX idx_api_usage_user ON api_usage(user_id, created_at);
CREATE INDEX idx_file_relationships ON file_relationships(source_file_id, relationship_type);
CREATE INDEX idx_analysis_language ON analysis_results(language);
CREATE INDEX idx_analysis_content_hash ON analysis_results(content_hash);

-- Modificar tabla files para remover campos de almacenamiento físico
ALTER TABLE files
    DROP COLUMN IF EXISTS file_path,
    MODIFY COLUMN filename VARCHAR(1024) NOT NULL COMMENT 'Ruta completa al archivo original';

-- Eliminar tabla de versiones ya que no almacenaremos archivos
DROP TABLE IF EXISTS file_versions;