from PennCourses.docs_settings import reverse_func


# See backend/PennCourses/docs_settings.py for more info on how to format these examples files.

ScheduleViewSet_examples = {
    reverse_func("schedules-list"): {
        "GET": {
            "requests": [],
            "responses": [
                {
                    "code": 200,
                    "summary": "GET List Schedules",
                    "value": [
                        {
                            "id": 1,
                            "sections": [
                                {
                                    "id": "CIS-120-001",
                                    "status": "O",
                                    "activity": "LEC",
                                    "credits": 1.0,
                                    "semester": "2020C",
                                    "meetings": [
                                        {"day": "F", "start": 11.0, "end": 12.0, "room": " "},
                                        {"day": "M", "start": 11.0, "end": 12.0, "room": " "},
                                        {"day": "W", "start": 11.0, "end": 12.0, "room": " "},
                                    ],
                                    "instructors": ["Swapneel Sheth", "Stephan A. Zdancewic"],
                                    "course_quality": 2.76,
                                    "instructor_quality": 3.17,
                                    "difficulty": 3.08,
                                    "work_required": 3.35,
                                    "associated_sections": [
                                        {"id": 1476, "activity": "REC"},
                                        {"id": 1477, "activity": "REC"},
                                        {"id": 1478, "activity": "REC"},
                                        {"id": 1479, "activity": "REC"},
                                        {"id": 1480, "activity": "REC"},
                                        {"id": 1481, "activity": "REC"},
                                        {"id": 1482, "activity": "REC"},
                                        {"id": 1483, "activity": "REC"},
                                        {"id": 1484, "activity": "REC"},
                                        {"id": 1485, "activity": "REC"},
                                        {"id": 1486, "activity": "REC"},
                                        {"id": 1487, "activity": "REC"},
                                        {"id": 1488, "activity": "REC"},
                                        {"id": 1489, "activity": "REC"},
                                        {"id": 1490, "activity": "REC"},
                                        {"id": 1491, "activity": "REC"},
                                        {"id": 1492, "activity": "REC"},
                                        {"id": 1493, "activity": "REC"},
                                        {"id": 1494, "activity": "REC"},
                                        {"id": 1495, "activity": "REC"},
                                    ],
                                },
                                {
                                    "id": "CIS-160-001",
                                    "status": "C",
                                    "activity": "LEC",
                                    "credits": 1.0,
                                    "semester": "2020C",
                                    "meetings": [
                                        {"day": "R", "start": 9.0, "end": 10.3, "room": " "},
                                        {"day": "T", "start": 9.0, "end": 10.3, "room": " "},
                                    ],
                                    "instructors": ["Rajiv C Gandhi"],
                                    "course_quality": 2.76,
                                    "instructor_quality": 3.17,
                                    "difficulty": 3.08,
                                    "work_required": 3.35,
                                    "associated_sections": [
                                        {"id": 1538, "activity": "REC"},
                                        {"id": 1539, "activity": "REC"},
                                        {"id": 1540, "activity": "REC"},
                                        {"id": 1541, "activity": "REC"},
                                        {"id": 1542, "activity": "REC"},
                                        {"id": 1543, "activity": "REC"},
                                        {"id": 1544, "activity": "REC"},
                                        {"id": 1545, "activity": "REC"},
                                        {"id": 1546, "activity": "REC"},
                                        {"id": 1547, "activity": "REC"},
                                        {"id": 1548, "activity": "REC"},
                                        {"id": 1549, "activity": "REC"},
                                        {"id": 1550, "activity": "REC"},
                                        {"id": 1551, "activity": "REC"},
                                        {"id": 1552, "activity": "REC"},
                                        {"id": 1553, "activity": "REC"},
                                        {"id": 1554, "activity": "REC"},
                                        {"id": 1555, "activity": "REC"},
                                        {"id": 1556, "activity": "REC"},
                                        {"id": 1557, "activity": "REC"},
                                        {"id": 1558, "activity": "REC"},
                                        {"id": 1559, "activity": "REC"},
                                        {"id": 1560, "activity": "REC"},
                                        {"id": 1561, "activity": "REC"},
                                        {"id": 1562, "activity": "REC"},
                                        {"id": 1563, "activity": "REC"},
                                        {"id": 1564, "activity": "REC"},
                                        {"id": 1565, "activity": "REC"},
                                        {"id": 1566, "activity": "REC"},
                                        {"id": 1567, "activity": "REC"},
                                        {"id": 1568, "activity": "REC"},
                                        {"id": 1569, "activity": "REC"},
                                        {"id": 1570, "activity": "REC"},
                                        {"id": 1571, "activity": "REC"},
                                        {"id": 1572, "activity": "REC"},
                                        {"id": 1573, "activity": "REC"},
                                    ],
                                },
                            ],
                            "semester": "2020C",
                            "name": "Fall 2020 Only CIS",
                            "created_at": "2020-08-17T18:10:49.464415-04:00",
                            "updated_at": "2020-08-17T18:10:49.464451-04:00",
                        },
                    ],
                }
            ],
        },
        "POST": {
            "requests": [
                {
                    "summary": "Minimally Customized POST",
                    "value": {
                        "name": "Fall 2020 Only CIS",
                        "sections": [
                            {"id": "CIS-120-001", "semester": "2020C"},
                            {"id": "CIS-160-001", "semester": "2020C"},
                        ],
                    },
                },
                {
                    "summary": "Maximally Customized POST",
                    "value": {
                        "id": 14,
                        "name": "Fall 2020 Only CIS",
                        "semester": "2020C",
                        "sections": [
                            {"id": "CIS-120-001", "semester": "2020C"},
                            {"id": "CIS-160-001", "semester": "2020C"},
                        ],
                    },
                },
            ],
            "responses": [],
        },
    },
    reverse_func("schedules-detail", args=["id"]): {
        "GET": {
            "requests": [],
            "responses": [
                {
                    "code": 200,
                    "summary": "GET Specific Schedule",
                    "value": {
                        "id": 1,
                        "sections": [
                            {
                                "id": "CIS-120-001",
                                "status": "O",
                                "activity": "LEC",
                                "credits": 1.0,
                                "semester": "2020C",
                                "meetings": [
                                    {"day": "F", "start": 11.0, "end": 12.0, "room": " "},
                                    {"day": "M", "start": 11.0, "end": 12.0, "room": " "},
                                    {"day": "W", "start": 11.0, "end": 12.0, "room": " "},
                                ],
                                "instructors": ["Swapneel Sheth", "Stephan A. Zdancewic"],
                                "course_quality": 2.76,
                                "instructor_quality": 3.17,
                                "difficulty": 3.08,
                                "work_required": 3.35,
                                "associated_sections": [
                                    {"id": 1476, "activity": "REC"},
                                    {"id": 1477, "activity": "REC"},
                                    {"id": 1478, "activity": "REC"},
                                    {"id": 1479, "activity": "REC"},
                                    {"id": 1480, "activity": "REC"},
                                    {"id": 1481, "activity": "REC"},
                                    {"id": 1482, "activity": "REC"},
                                    {"id": 1483, "activity": "REC"},
                                    {"id": 1484, "activity": "REC"},
                                    {"id": 1485, "activity": "REC"},
                                    {"id": 1486, "activity": "REC"},
                                    {"id": 1487, "activity": "REC"},
                                    {"id": 1488, "activity": "REC"},
                                    {"id": 1489, "activity": "REC"},
                                    {"id": 1490, "activity": "REC"},
                                    {"id": 1491, "activity": "REC"},
                                    {"id": 1492, "activity": "REC"},
                                    {"id": 1493, "activity": "REC"},
                                    {"id": 1494, "activity": "REC"},
                                    {"id": 1495, "activity": "REC"},
                                ],
                            },
                            {
                                "id": "CIS-160-001",
                                "status": "C",
                                "activity": "LEC",
                                "credits": 1.0,
                                "semester": "2020C",
                                "meetings": [
                                    {"day": "R", "start": 9.0, "end": 10.3, "room": " "},
                                    {"day": "T", "start": 9.0, "end": 10.3, "room": " "},
                                ],
                                "instructors": ["Rajiv C Gandhi"],
                                "course_quality": 2.76,
                                "instructor_quality": 3.17,
                                "difficulty": 3.08,
                                "work_required": 3.35,
                                "associated_sections": [
                                    {"id": 1538, "activity": "REC"},
                                    {"id": 1539, "activity": "REC"},
                                    {"id": 1540, "activity": "REC"},
                                    {"id": 1541, "activity": "REC"},
                                    {"id": 1542, "activity": "REC"},
                                    {"id": 1543, "activity": "REC"},
                                    {"id": 1544, "activity": "REC"},
                                    {"id": 1545, "activity": "REC"},
                                    {"id": 1546, "activity": "REC"},
                                    {"id": 1547, "activity": "REC"},
                                    {"id": 1548, "activity": "REC"},
                                    {"id": 1549, "activity": "REC"},
                                    {"id": 1550, "activity": "REC"},
                                    {"id": 1551, "activity": "REC"},
                                    {"id": 1552, "activity": "REC"},
                                    {"id": 1553, "activity": "REC"},
                                    {"id": 1554, "activity": "REC"},
                                    {"id": 1555, "activity": "REC"},
                                    {"id": 1556, "activity": "REC"},
                                    {"id": 1557, "activity": "REC"},
                                    {"id": 1558, "activity": "REC"},
                                    {"id": 1559, "activity": "REC"},
                                    {"id": 1560, "activity": "REC"},
                                    {"id": 1561, "activity": "REC"},
                                    {"id": 1562, "activity": "REC"},
                                    {"id": 1563, "activity": "REC"},
                                    {"id": 1564, "activity": "REC"},
                                    {"id": 1565, "activity": "REC"},
                                    {"id": 1566, "activity": "REC"},
                                    {"id": 1567, "activity": "REC"},
                                    {"id": 1568, "activity": "REC"},
                                    {"id": 1569, "activity": "REC"},
                                    {"id": 1570, "activity": "REC"},
                                    {"id": 1571, "activity": "REC"},
                                    {"id": 1572, "activity": "REC"},
                                    {"id": 1573, "activity": "REC"},
                                ],
                            },
                        ],
                        "semester": "2020C",
                        "name": "Fall 2020 Only CIS",
                        "created_at": "2020-08-17T18:10:49.464415-04:00",
                        "updated_at": "2020-08-17T18:10:49.464451-04:00",
                    },
                }
            ],
        },
        "PUT": {
            "requests": [
                {
                    "summary": "Minimally Customized PUT",
                    "value": {
                        "name": "Fall 2020 Only CIS New",
                        "sections": [
                            {"id": "CIS-120-002", "semester": "2020C"},
                            {"id": "CIS-160-002", "semester": "2020C"},
                        ],
                    },
                },
                {
                    "summary": "Maximally Customized PUT",
                    "value": {
                        "name": "Fall 2020 Only CIS New",
                        "semester": "2020C",
                        "sections": [
                            {"id": "CIS-120-002", "semester": "2020C"},
                            {"id": "CIS-160-002", "semester": "2020C"},
                        ],
                    },
                },
            ],
            "responses": [],
        },
    },
}
