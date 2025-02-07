"""
Definition of the :class:`Profile` model.
"""
from accounts.models.choices import Title
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """
    A user profile, associated to each user using a OneToOne relationship and
    created automatically usings signals.

    References
    ----------
    * `Extending the User model`_.

    .. _Extending the User model:
       https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

    """

    #: OneToOne relationship with the user model.
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )

    #: Academic or any other kind of title.
    title = models.CharField(
        max_length=20,
        choices=Title.choices(),
        default="",
        blank=True,
        null=True,
    )

    #: Profile image.
    image = models.ImageField(upload_to="images/profiles", blank=True)

    #: User's date of birth.
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    #: The institute to which a user belongs, if any.
    institute = models.CharField(max_length=255, blank=True, null=True)

    #: Short user biography.
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return self.user.get_full_name()

    def get_absolute_url(self) -> str:
        """
        Returns the canonical URL for this instance.

        References
        ----------
        * `get_absolute_url()`_

        .. _get_absolute_url():
           https://docs.djangoproject.com/en/3.0/ref/models/instances/#get-absolute-url

        Returns
        -------
        str
            URL
        """
        return reverse("accounts:user-detail", args=[str(self.user.id)])

    def get_title_repr(self) -> str:
        """
        Returns the verbose title of the user as defined in the
        :class:`~accounts.models.choices.Title` Enum.

        Returns
        -------
        str
            Verbose title representation
        """
        try:
            return Title[self.title].value
        except (KeyError, ValueError):
            pass

    def get_full_name(self, include_title: bool = True) -> str:
        """
        Returns the full name of the user, including a title if any.

        Parameters
        ----------
        include_title : bool, optional
            Whether to include title (academic credentials etc.) if specified

        Returns
        -------
        str
            User's full name
        """

        full_name = self.user.get_full_name()
        if include_title and self.title:
            title = self.get_title_repr()
            return f"{full_name}, {title}"
        return full_name
