import esmtp
from getpass import getpass


def main() -> None:
    host = input("Enter SMTP server hostname (example: smtp.test.com): ")
    username = input("Enter your username (e-mail): ")
    password = getpass("Enter your password: ")
    esmtp.run(host, [username, password])


if __name__ == "__main__":
    main()
