(1) loop = asyncio.get_event_loop()

Вам необходим некий экземпляр цикла прежде чем вы можете запустить какие бы то ни было сопрограммы, а это именно он и есть. На самом деле, где бы вы его не вызывали, get_event_loop() предоставит вам всякий раз тот же самый экземпляр loop, раз уж вы используете только один единственный поток. [API asyncio позволяет вам делать много безумных вещей с несколькими экземплярами и потоками циклов, но данная книга не является самой подходящей книгой для данной цели. 99% общего времени вы будете использовать некий единичный, основной поток для своей прикладной программы, как это показано тут.]

(2) task = loop.create_task(coro)

В приведённом выше коде loop.create_task(main()) является неким особенным вызовом. Ваша функция сопрограммы не будет исполняться пока вы не сделает его. Мы говорим, что create_task() планирует исполнение вашей сопрограммы в данном цикле. Возвращаемый объект task может применяться для отслеживания текущего состояния данной задачи, например, исполняется ди она ещё или уже выполнена, а помимо этого может также применяться для получения некоторого результирующего значения от вашей завершённой сопрограммы. Вы также можете завершать данную задачу при помощи task.cancel(). [с другой стороны: вы можете заметить в этой строке кода что основным параметром в таком вызове функции для create_task() является coro. Именно это соглашение используется в большей части документации API, которую вы обнаружите, и он ссылается на некую coroutine; т.е., строго говоря, собственно результат вызова некоторой функции async def, а не саму эту функцию.]

(3) loop.run_until_complete(coro) и loop.run_forever()

Это два способа запуска данного цикла. Они оба заблокируют данный текущий поток, которым обычно является самый основной поток {main}. Отметим, что run_until_complete() сохранит данный цикл исполняемым до тех пор, пока не завершится заданный coro - но все прочие запланированные задачи в этом цикле также будут исполняться при выполнении данного цикла.

(4) group = asyncio.gather(task1, task2, task3)

Типичная манера для большинства программ будет состоять в том, чтобы начаться с loop.run_forever() для самой "главной" части ваше программы {main} , а затем, когда получен некий сигнал процесса, остановить данный цикл, собрать всё ещё приостановленные задачи, а затем воспользоваться loop.run_until_complete() до тех пор, пока эти задачи не выполнятся. именно этот метод служит для выполнения сбора. В более общем плане он также может применяться для сбора множества сопрограмм воедино и ожидания (при помощи await!) пока все собранные задачи не завершатся.

(5) loop.stop() и loop.close()

Как уже описано выше, они применяются для постепенного останова некоторой программы. stop() обычно вызывается как следствие получения некоторого сигнала выключения, а close() обычно является самым последним действием: и оно очистит все очереди и остановит Исполнителя {Executor}. "Остановленный" цикл может быть запущен вновь, а "закрытый" цикл исчезает навсегда.

[Предостережение]	Предостережение
Предыдущий пример является слишком упрощённым чтобы применяться в практических настройках. Требуется дополнительная информация относительно обработки правильного останова. Основной целью данного примера было просто представить большую часть важнейших функций и методов из asyncio. Дополнительная практическая информация по обработке останова представлена позднее в данной книге.


syncio в Python представляет множество базовых механизмов вокруг основного цикла событий - и требует чтобы вы были осведомлены о таких вещах, как сам цикл событий и управление им на протяжении его времени жизни. Именно это является отличием, например, от Node.js, который также содержит некий цикл событий, но сохраняет его где- то вовне в скрытом виде. Однако, как только вы начнёте понемногу работать с asyncio, вы начнёте замечать, что ваш шаблон запуска и останова основного цикла событий не отходит страшно далеко от приведённого выше кода. А в оставшейся части данной книги мы рассмотрим более подробно некоторые нюансы относительно времени жизни цикла.

В приведённом выше примере я кое- что упустил. Самый последний элемент базовой функциональности, о котором вам следует знать, состоит в том как запускать блокирующие функции. Основной момент относительно кооперативной многозадачности состоит в том, что вам требуется все связанные с вводом/ выводом функции..., ну да, кооперировать, а это означает допуск переключения некоторого контекста обратно в данный цикл при помощи особого ключевого слова await. Большая часть имеющегося кода Python, доступного на текущий момент в диком виде, не делает этого, а вместо этого полагается на вас для запуска таких функций в потоках. До тех пор, пока не будет более широко распространённой поддержки функций async def, вы обнаружите, что применение таких библиотек с блокировкой неизбежно.

Для этого asyncio предоставляет некий API, который очень похож на API из пакета concurrent.futures. Данный пакет предоставляет некий ThreadPoolExecutor и какой- тоProcessPoolExecutor. По умолчанию он основан на потоке, но запросто заменяется на базирование на процессе. Я опустил это в своём предыдущем примере, так как это скрыло бы то описание, как подгоняются друг к другу все фундаментальные части. Теперь, когда они были обсуждены, мы можем взглянуть непосредственно на исполнителя.