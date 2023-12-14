### 
___ - игра, в которой пользователю предстоит выживать под внушительным натиском противников, часть из которых способна напрямую преследовать игрока. В игре присутствуют 3 типа управления, упорядоченные по
уровню сложности. Выбор управления предоставлен пользователю в главном меню игры.
### Требования
Для запуска игры на вашем компьютере должен быть установлен Python версии 3+ с библиотеками:
- numpy
- pygame

Чтобы установить данные библиотеки, введите в командную строку следующее:

`pip install numpy`

`pip install pygame`
### Управление
Как было упомянуто выше, в игре существует 3 типа управления.
# 1 тип
Пользователь управляет объектом используя соответствующие стрелки на клавиатуре.
# 2 тип
Объект игрока движется в направлении курсора мыши.
# 3 тип
Объект движется под действием постоянной силы, направление которой выбирает пользователь стрелками на клавиатуре. Есть функция торможения, реализуемая нажатием клавиши "пробел".
