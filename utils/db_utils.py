import pyodbc

class OTPNotFoundError(Exception):
    """Custom exception raised when no OTP is found for the given email."""
    pass


class DatabaseUtils:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection_string(self):
        """Build and return a secure SQL Server connection string."""
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.host};"
            f"DATABASE={self.database};"
            f"UID={self.user};"
            f"PWD={self.password};"
        )

    def get_otp(self, email: str) -> str:
        """
        Fetch the latest OTP for a specific email from Microsoft SQL Server.
        Raises OTPNotFoundError if no OTP is found.
        """
        if not email:
            raise ValueError("Email must not be empty.")

        connection_str = self.get_connection_string()

        try:
            # Use context manager to ensure resources are closed automatically
            with pyodbc.connect(connection_str, timeout=10) as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT TOP 1 OtpCode
                    FROM EmailOtps
                    WHERE Email = ?
                    ORDER BY CreatedAt DESC
                    """
                    cursor.execute(query, (email,))
                    result = cursor.fetchone()

            if result:
                return str(result[0])
            else:
                raise OTPNotFoundError(f"No OTP found for email: {email}")

        except pyodbc.InterfaceError:
            raise ConnectionError("Failed to connect to the SQL Server. Check your host or credentials.")
        except pyodbc.ProgrammingError as e:
            raise RuntimeError(f"SQL syntax error or invalid table/column: {e}")
        except pyodbc.Error as e:
            raise RuntimeError(f"Database error: {e}")


