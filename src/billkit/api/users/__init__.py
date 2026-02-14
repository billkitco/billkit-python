import os
from collections.abc import Callable

from ...models.users import LogoUploadResponse, PartialUserDetails, UserDetails


class Users:
    def __init__(self, requester: Callable) -> None:
        self._requester = requester

    def get_user(self) -> UserDetails:
        """
        Fetch the current user's profile details.

        Returns:
            UserDetails: The authenticated user's profile data.

        Example:
            user = client.users.get_user()
            print(user.email)
        """
        response_data = self._requester("GET", "users/me")
        return UserDetails(**response_data)

    def patch_user(self, user_details: PartialUserDetails) -> UserDetails:
        """
        Update the current user's profile with partial details.

        Args:
            user_details: Fields to update (unset fields are ignored).

        Returns:
            UserDetails: The updated user profile.

        Raises:
            HTTPException: If update fails (e.g., invalid data).

        Example:
            updates = PartialUserDetails(name="New Name")
            updated_user = client.users.patch_user(updates)
        """
        response_data = self._requester(
            "PATCH", "users/me", json=user_details.model_dump(exclude_unset=True)
        )
        return UserDetails(**response_data)

    def upload_logo(self, image_path: os.PathLike[str]) -> LogoUploadResponse:
        """
        Upload a logo image to the user profile.

        The uploaded logo URL will be available via `BillkitClient.users.get_user().logo_url`.

        Args:
            image_path: Path to the image file (JPG, PNG, or WebP recommended, max 5MB)

        Returns:
            The API response containing upload metadata.

        Example:
            client.users.upload_logo("path/to/logo.png")
            user = client.users.get_user()
            print(user.logo_url)  # Use the new logo
        """
        with open(os.fspath(image_path), "rb") as f:
            files = {"file": f}
            response_data = self._requester("POST", "users/logo", files=files)
        return LogoUploadResponse(**response_data)
