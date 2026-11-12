from models.user_model import User
import uuid
from Helpers import import_data

class User_logic:
    def add_user() -> bool:
        print("============ CREATE USER ============")
        try: 
            name = input("Name: ")
            user_uid = str(uuid.uuid4().hex)

            if not name.strip():
                print("Name is required.")
                return False
            import_data.save_user(User(name.strip(), user_uid))
        except ValueError as e:
            print("Invalid input. Error: ", e)
            return False

        return True

    def get_user_by_uid(user_uid: str) -> User | None:
        """Retrieve a specific user by their unique identifier."""
        users = import_data._load_json_db(import_data.USER_DB_PATH)
        for u in users:
            if u.get("uid") == user_uid:
                return User(name=u.get("name"), uid=u.get("uid"))
        return None

    def get_all_users() -> list[User]:
        """Retrieve all users from the database."""
        users = import_data._load_json_db(import_data.USER_DB_PATH)
        return [User(name=u.get("name"), uid=u.get("uid")) for u in users]

    def delete_user(user_uid: str):
        """Delete a user by UID and remove all associated orders."""
        # 1. Remove user from user database
        users = import_data._load_json_db(import_data.USER_DB_PATH)
        filtered_users = [u for u in users if u.get("uid") != user_uid]
        import_data._save_json_db(import_data.USER_DB_PATH, filtered_users)

        # 2. Remove all orders associated with the user from the order database
        orders = import_data._load_json_db(import_data.ORDER_DB_PATH)
        filtered_orders = [o for o in orders if o.get("user_uid") != user_uid]
        import_data._save_json_db(import_data.ORDER_DB_PATH, filtered_orders)