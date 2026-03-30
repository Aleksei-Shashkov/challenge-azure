IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TrainDepartures' AND xtype='U')
CREATE TABLE TrainDepartures (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Station NVARCHAR(100),
    Vehicle NVARCHAR(100),
    DepartureTime DATETIME,
    Delay INT,
    Platform NVARCHAR(50),
    Destination NVARCHAR(100)
);

-- Пересоздаем нашего пользователя "силовым" методом
DROP USER IF EXISTS [train_user];
CREATE USER [train_user] WITH PASSWORD = 'Ifirjd@12';
ALTER ROLE db_owner ADD MEMBER [train_user];