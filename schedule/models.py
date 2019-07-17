from django.db import models
import json, requests


# Create your models here.
class Group(models.Model):  # Absolete
    group = models.IntegerField()
    group_id = models.IntegerField()

    def __str__(self):  # Do I need this?
        return str(self.group)

    def fill(self):
        """
        Fill table "Group" with data
        :return: <String>
        """
        url = "https://kai.ru/raspisanie"
        for num in range(1, 10):
            data = {
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_state": "normal",
                "p_p_mode": "view",
                "p_p_resource_id": "getGroupsURL",
                "p_p_cacheability": "cacheLevelPage",
                "p_p_col_id": "column-1",
                "p_p_col_count": "1",
                "query": str(num)  # variable
            }
            j = json.loads(requests.post(url=url, data=data).content.decode("cp1251"))
            for group in j:
                q = Group(group=group["group"], group_id=group["id"])
                q.save()
        return "Table Group has been filled"


class Schedule(models.Model):
    group = models.IntegerField()
    weekday = models.CharField(max_length=11)
    time = models.CharField(max_length=5)
    date = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    classroom = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    professor = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):  # Do I need this?
        return "%s %s %s %s" % (str(self.group), self.weekday, self.time, self.name)

    def fill(self):
        """
        Filling Schedule table(~5 minutes)
        Don't be stunned by a lot of mondays
        :return: <String>
        """
        weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

        for group in Group.objects.all():
            url = "https://kai.ru/raspisanie"
            data = {
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_state": "normal",
                "p_p_mode": "view",
                "p_p_resource_id": "schedule",
                "p_p_cacheability": "cacheLevelPage",
                "p_p_col_id": "column-1",
                "p_p_col_count": "1",
                "groupId": group.group_id
            }
            table = requests.post(url=url, data=data).content.decode("utf-8")
            table = json.loads(table)
            for weekday in table:
                for cls in table[str(weekday)]:
                    q = Schedule()
                    q.group = group.group
                    q.weekday = weekdays[int(weekday)-1]
                    q.time = cls["dayTime"].strip()
                    q.date = cls["dayDate"].strip()
                    q.name = cls["disciplName"].strip()
                    q.type = cls["disciplType"].strip()
                    q.classroom = cls["audNum"].strip()
                    q.building = cls["buildNum"].strip()
                    q.professor = cls["prepodName"].strip()
                    q.department = cls["orgUnitName"].strip()
                    q.save()

        return "Table Schedule has been filled"
