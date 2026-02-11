from collections.abc import Callable
from ...models.users import UserDetails, PartialUserDetails


class Users:
    def __init__(self, requester: Callable) -> None:
        self.requester = requester

    def get_user(self) -> UserDetails:
        """Return the current user as a `UserDetails` model."""
        response_data = self.requester("GET", "users/me")
        return UserDetails(**response_data)

    def patch_user(self, user_details: PartialUserDetails) -> UserDetails:
        response_data = self.requester(
            "PATCH",
            "users/me",
            json=user_details.model_dump(exclude_unset=True)
        )
        return UserDetails(**response_data)
    