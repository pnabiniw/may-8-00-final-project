"""
What are the differences in .get() and .filter() ORMs?
"""

# get() returns objects
# filter() returns a queryset

# Student.objects.get(id=100) => ObjectDoesNotExist
# Student.objects.get(name="Raj") => MultipleObjectsReturned
