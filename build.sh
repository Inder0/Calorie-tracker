#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py migrate

python manage.py shell <<EOF
from food.models import FoodItem
from django.core.management import call_command

if FoodItem.objects.count() == 0:
    call_command('loaddata', 'food_items.json')
EOF

python manage.py collectstatic --noinput