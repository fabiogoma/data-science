SELECT * FROM worldcup

SELECT Year, Champions FROM worldcup WHERE Champions = 'Brazil'

SELECT Year, "Fair play award" FROM worldcup WHERE "Fair play award" LIKE "%Brazil%"

SELECT Champions, count(Champions) as Titles  FROM worldcup GROUP BY Champions ORDER BY Titles DESC

SELECT "Runners-up", count("Runners-up") as Titles FROM worldcup GROUP BY "Runners-up" ORDER BY Titles DESC

SELECT "Third place", count("Third place") as Titles FROM worldcup GROUP BY "Third place" ORDER BY Titles DESC

SELECT "Fourth place", count("Fourth place") as Titles FROM worldcup GROUP BY "Fourth place" ORDER BY Titles DESC

SELECT Year, Attendance, "Host country" FROM worldcup ORDER BY Attendance DESC LIMIT 10

SELECT Year, Attendance, "Host country" FROM worldcup ORDER BY Attendance DESC LIMIT 5
SELECT datetime('now','localtime') AS time, Year, Champions FROM worldcup ORDER BY Year

SELECT Year, Teams, "Host country" FROM worldcup ORDER BY Teams DESC LIMIT 5

SELECT Year, Stadiums, "Host country" FROM worldcup ORDER BY Stadiums DESC LIMIT 10

SELECT count("Host country") Times, "Host country" FROM worldcup GROUP BY "Host country" ORDER BY Times DESC LIMIT 5

SELECT Year, "Goals scored", "Host country" FROM worldcup ORDER BY "Goals scored" DESC LIMIT 10
