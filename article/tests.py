from django.test import TestCase

# Create your tests here.

a = [2,3,1,6,4]
a.sort()
print(a)

b = [(1,3),(5,2),(3,7),(6,4)]
# x代表b中的一个元素，此处代表一个元组，x[1]按照每个元组的第二个元素排序
b.sort(key=lambda x: x[0])
print(b)
b.sort(key=lambda x: x[1])
print(b)