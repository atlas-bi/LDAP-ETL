USE [master]
GO

CREATE DATABASE [LDAP]
 CONTAINMENT = NONE
GO

USE [LDAP]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Groups](
	[GroupId] [int] IDENTITY(1,1) NOT NULL,
	[AccountName] [nvarchar](max) NULL,
	[GroupName] [nvarchar](max) NULL,
	[GroupEmail] [nvarchar](max) NULL,
	[GroupType] [nvarchar](max) NULL,
	[LoadDate] [date],
PRIMARY KEY CLUSTERED
(
	[GroupId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Memberships](
	[MembershipId] [int] IDENTITY(1,1) NOT NULL,
	[AccountName] [nvarchar](max) NULL,
	[GroupType] [nvarchar](max) NULL,
	[GroupName] [nvarchar](max) NULL,
	[LoadDate] [date],
PRIMARY KEY CLUSTERED
(
	[MembershipId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[UserId] [int] IDENTITY(1,1) NOT NULL,
	[Base] [nvarchar](max) NULL,
	[EmployeeId] [nvarchar](max) NULL,
	[AccountName] [nvarchar](max) NULL,
	[DisplayName] [nvarchar](max) NULL,
	[FullName] [nvarchar](max) NULL,
	[FirstName] [nvarchar](max) NULL,
	[LastName] [nvarchar](max) NULL,
	[Department] [nvarchar](max) NULL,
	[Title] [nvarchar](max) NULL,
	[Phone] [nvarchar](max) NULL,
	[Email] [nvarchar](max) NULL,
	[LoadDate] [date],
PRIMARY KEY CLUSTERED
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [LDAP] SET  READ_WRITE
GO
