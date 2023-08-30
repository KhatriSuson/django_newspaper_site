

## 1 - 1 Relationship
# 1 user can have only 1 profile   => 1
# 1 profile is associated to only 1 user  => 1
# OneToOneField() => Any Model


## 1 - M Relationship
# 1 user can add M post  => M
# 1 post is associated to only 1 user => 1
# In django use ForeignKey() => Use in Many side Model

## M - M Relationship
# 1 student can learn from M teachers => M
# 1 teacher can teach M students => M
# ManyToManyField() => Any Place