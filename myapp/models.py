from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
#  Storing all food items the user wants in their profile
class Food(models.Model):
    name = models.CharField( max_length=200 ,null = False)
    quantity = models.PositiveIntegerField(null = False , default = 0)
    calorie = models. FloatField (null = False, default = 0)
    person_of = models.ForeignKey(User, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

#Stores all the required data for tracking calories
class Profile(models.Model):
    person_of = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    quantity = models.FloatField (default = 0)
    calorie_count = models.FloatField (default = 0 , null = True, blank = True) 
    food_selected = models.ForeignKey (Food , on_delete = models.CASCADE, null = True, blank = True)
    total_calorie = models.FloatField(default = 0, null = True)
    calorie_goal = models.PositiveIntegerField (default = 0)
    date = models.DateField(auto_now_add = True)
    all_food_selected = models.ManyToManyField(Food,through = 'PostFood', related_name = 'inventory')

    def save (self, *args, **kwargs):
     if self.food_selected != None:
        self.amount = (self.food_selected.calorie/self.food_selected.quantity)
        self.calorie_count = self.amount * self.quantity
        self.total_calorie = self.calorie_count + self.total_calorie
        calories = Profile.objects.filter(person_of = self.person_of).last ()
        PostFood.objects.create(profile= calories, food=self.food_selected,calorie_amount=self.calorie_count, amount=self.quantity)
        self.food_selected = None
        super(Profile, self).save(*args,**kwargs)

     else:
      super(Profile, self).save(*args,**kwargs)


    def __str__ (self):
        return str(self.person_of.username)
    
# Keeos track of all food consumed by the user
class PostFood(models.Model):
    profile=models.ForeignKey(Profile , on_delete= models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    calorie = models.FloatField(default = 0)
    amount = models.FloatField(default= 0, null = True)
    calorie_amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.profile.person_of.username} - {self.food.name}"
    
class MealLog(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    date = models.DateField(default=timezone.now)