#!/bin/bash

python3 update_quiz.py
git add .
git commit -m "update quiz"
git push origin newhome
