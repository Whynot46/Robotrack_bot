lessons = [('Робототехника', '10-14 лет', '10:00-11:40'), ('Робототехника', '7-9 лет', '16:20-18:00'), ('3D моделирование', '10+ лет', '18:20-20:00')]
lessons_msg = ""
for lesson in lessons:
    lessons_msg += f"{lesson}\n\n"

lessons_msg = lessons_msg.replace("(", "").replace(")", "").replace("'", "").replace(", ", "\n")

print(lessons_msg)
print("Вторник\n23232323".split('\n')[0])