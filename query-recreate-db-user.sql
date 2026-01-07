DROP USER IF EXISTS [train_user];
GO

-- 2. Создаем автономного пользователя с паролем
CREATE USER [train_user] WITH PASSWORD = 'Ifirjd@12';
GO

-- 3. Назначаем права владельца базы
ALTER ROLE db_owner ADD MEMBER [train_user];
GO