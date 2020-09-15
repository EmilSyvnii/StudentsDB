function initJournal() {
    var indicator = $('#ajax-progress-indicator');

    $('.day-box input[type="checkbox"]').click(function(event){
        var box = $(this);              /* змінна box зберігає посилання на поточний чекбокс */
        $.ajax(box.data('url'), {       /* 2 аргументи: адреса обробника запиту на сервері та словник з налаштуваннями */
            'type': 'POST',             /* урл витягується із атрибута data-url який встановлений у чекбоксах */
            'async': true,
            'dataType': 'json',
            'data': {                   /* дані, які будуть доступні у тілі POST */
                'pk': box.data('student-id'),       /* витягується і передається параметр IDшки студента */
                'date': box.data('date'),           /* дата поточного чекбокса */
                'present': box.is(':checked') ? '1': '',        /*  */
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                alert(error);
                indicator.hide();
            },
            'success': function(data, status, xhr){
                indicator.hide();
            }
        });
    });
}

function initGroupSelector() {
    /* функція, яка чіпляє код на подію change */
    $('#group-selector select').change(function(event){         // пошук випадайки через селектор
    var group = $(this).val();                                  // отримання значення тегу option, тобто саму групу

    if (group) {
        $.cookie('current_group', group, {'path': '/', 'expires': 365});
    } else {
        $.removeCookie('current_group', {'path': '/'});         // якшо жодної групи не було обрано, створена кука видаляється
        }
        location.reload(true);          // перевантаження сторінки

        return true;
    });
}

function initDateFields() {
    $('input.dateinput').datetimepicker({'format': 'YYYY-MM-DD'});
}

function initEditStudentPage() {
    $('a.student-edit-form-link').click(function(event) {
        var link = $(this);                             // запам'ятовується лінк, по якому клікнули
        $.ajax({                                        // AJAX-запит на сервер для відображення форми у модальному вікні
            'url': link.attr('href'),                   // передача адреси, на яку потрібно зробити запит
                                                        // (адреса береться з атрибута (href))
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){
                if (status != 'success') {              // перевірка на успішність зробленого запиту
                    alert('Помилка на сервері, повторіть спробу пізніше.');
                    return false;
                }

                var modal = $('#myModal'), html = $(data), form = html.find('#content-column form');
                    /* 1. пошук контейнера модального вікна всередині обробника
                       2. отримуються дані із html-дока і перетворюються у jQuery-об'єкт для подальшої маніпуляції
                       3. пошук конкретних елементів із темплейту */
                modal.find('.modal-title').html(html.find('#content-column h2').text());  // витягується текст заголовку
                modal.find('.modal-body').html(form);           // передача самої форми

                initEditStudentForm(form, modal);               // виклик функції форми

                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true                    // показується знайдене вікно за доп. методу modal
                });
            },                                          //  із jQuery бібл. та аргументом 'show'
            'error': function(){
                alert('Помилка на сервері, повторіть спробу пізніше.');
                return false;
            }
        });

        return false;                // повернути false щоб ігнорувати подію і не застосовувати власного обробника
    });
}

function initEditStudentForm(form, modal) {
    // приєднання віджета календаря до усіх полів з датами
    initDateFields();

    form.find('input[name="cancel_button"]').click(function(event){
        modal.modal('hide');
        return false;
    });

    // робота форми через AJAX
    form.ajaxForm({
        'dataType': 'html',
        'error': function(){
            alert ('Помилка на сервері, повторіть спробу пізніше.');
            return false;
        },
        'success': function(data, status, xhr) {
            var html = $(data), newform = html.find('#content-column form');
            modal.find('.modal-body').html(html.find('.alert'));
            if (newform.length > 0) {                           // перевірка чи нова форма знайдена
                modal.find('.modal-body').append(newform);
                initEditStudentForm(newform, modal);
            } else {
                setTimeout(function(){location.reload(true);}, 500);
            }
        }
    });
}

$(document).ready(function(){        // функції, які викликаються лише після повного завантаження сторінки
    initJournal();
    initGroupSelector();
    initDateFields();
    initEditStudentPage();
});