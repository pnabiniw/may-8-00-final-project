"""
What are related names and how can we use it?
"""

"""User
    name

UserProfile
    => user = models.OneOne(User)
    => address


user.userprofile.address

User.objects.filter(userprofile__address='KTM')"""