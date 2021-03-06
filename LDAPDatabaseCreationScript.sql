USE [master]
GO

CREATE DATABASE [LDAP]
 CONTAINMENT = NONE
GO
ALTER DATABASE [LDAP] SET COMPATIBILITY_LEVEL = 130
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [LDAP].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [LDAP] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [LDAP] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [LDAP] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [LDAP] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [LDAP] SET ARITHABORT OFF 
GO
ALTER DATABASE [LDAP] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [LDAP] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [LDAP] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [LDAP] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [LDAP] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [LDAP] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [LDAP] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [LDAP] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [LDAP] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [LDAP] SET  DISABLE_BROKER 
GO
ALTER DATABASE [LDAP] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [LDAP] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [LDAP] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [LDAP] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [LDAP] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [LDAP] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [LDAP] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [LDAP] SET RECOVERY FULL 
GO
ALTER DATABASE [LDAP] SET  MULTI_USER 
GO
ALTER DATABASE [LDAP] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [LDAP] SET DB_CHAINING OFF 
GO
ALTER DATABASE [LDAP] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [LDAP] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [LDAP] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [LDAP] SET QUERY_STORE = OFF
GO
USE [LDAP]
GO
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
GO
USE [LDAP]
GO


ALTER ROLE [db_datareader] ADD MEMBER [datagov]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [datagov]
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
