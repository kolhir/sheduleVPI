
var number;
var day;
var week;
var teach_list = {};
// var teach_list = {0:"Выберете преподавателя", 1:"Рыбанов А.А", 2:"Короткова Н.Н", 3:"Абрамова О.Ф.", 4:"Саньков С.Г"}
// var lesson_list = {0:"Выберете предмет", 1:"Базы данных", 2:"Исследовние операций", 3:"Компьютерная грамотность", 4:"Операционые системы"}
var room_list = {0:"Выберете аудиторию", 1:"В-201", 2:"В-202", 3:"В-206", 4:"А-21"};
// var korpus_list = {0:"", 1:"А", 2:"В", 3:"Б"}
var type_list = {0:"Выберете тип занятия", 1:"Лекция", 2:"Практика", 3:"Лабораторная"};
var week_c = {"first" : "Первая неделя", "second": "Вторая неделя"};
var day_c = {mon : "Понедельник",
             tues: "Вторник",
             wen: "Среда",
             thurs: "Четверг",
             fri: "Пятница",
             sat: "Суббота"
            };

// function gen_tacher_list():

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {

    // $.ajax({
    //    url: '/',
    //    method: 'POST',
    //    data: data,
    //    success: function(d) {
    //    // console.log(d);
    //    },
    //    error: function(d) {
    //    // console.log(d);
    //    }
   });
class TimeTableInfo{

}

var data = {};
class ModalForAdd {
  constructor (){
      this.generateModal()
  }

  newLesson(number, day, week) {
        this.number = number
        this.day = day
        this.week = week
  }

  generateModal()  {
      $('#name').empty()
      $('#teach').empty()
      $('#korpus').empty()
      $('#room').empty()
      $('#type').empty()

      $.each(lesson_list, function(key,  value) {
        $('#name').append('<option value="' + key + '">' + value + '</option>');

      });

      // $.each(teach_list, function(key,  value) {
      //   $('#teach').append('<option value="' + key + '">' + value + '</option>');

      // });

      $.each(korpus_list, function(key,  value) {
        $('#korpus').append('<option value="' + key + '">' + value + '</option>');

      });

      // $.each(room_list, function(key,  value) {
      //   $('#room').append('<option value="' + key + '">' + value + '</option>');

      // });
      $.each(type_list, function(key,  value) {
        $('#type').append('<option value="' + key + '">' + value + '</option>');

      });
    }

    fill_teach(teach_list){
      $('#teach').empty()
      $.each(teach_list, function(key,  value) {
        $('#teach').append('<option value="' + key + '">' + value + '</option>');

      });
    }

    fill_room(room_list){
      $('#room').empty()
      $.each(room_list, function(key,  value) {
        $('#room').append('<option value="' + key + '">' + value + '</option>');

      });
    }

    fill_info (teach_list) {
            $(".week_modal").empty()
            $(".week_modal").append(`<strong>${week_c[this.week]}</strong>`)

            $(".day_modal").empty()
            $(".day_modal").append(`<i>${day_c[this.day]}, ${parseInt(this.number)} пара</i>`)

            $('#modal_error').empty()
    }

    show() {
        this.fill_info()
        $("#addLesson").modal('show');
    }

    hide() {
      $("#addLesson").modal('hide');
      // this.generateModal()
      timetable.save_changes_ajax()
    }

    show_error () {
      $('#modal_error').empty()
      $('#modal_error').append(`<div class="alert alert-warning" role="alert">Заполните все поля</div>`)
    }

    validate () {
      if (modal_add.check_value(modal_add.get_data()) != false)
      {
        return true
      } else {
        this.show_error()

      }
    }

    get_data () {
      $('#addLesson').find ('select').each(function() {
        data[this.name] = $(this).val();

      });
      return data
    }

    check_value () {
      var flag = true
      $.each(data, function(key, value) {
        if (value === "0")
        {
          flag = false
        }
     });
     return flag
    }
  }


var modal_add = new ModalForAdd()
var current_cell = null

$('.cell-lesson').click(function (event) {
    current_cell = $(this)
    number = $(this).attr("class").match(/\w+|"[^"]+"/g)[0][1]
    day = $(this).parent().attr("class").match(/\w+|"[^"]+"/g)[0]
    week = $(this).parent().parent().attr("class").match(/\w+|"[^"]+"/g)[0]
    modal_add.newLesson(number, day, week)
    modal_add.show()
});

$('.name-lesson').change(function(event) {
  // alert()

  var json_data = {"name":$('.name-lesson option:selected').text()}
  $.ajax({
     url: '/get_teacher',
     method: 'POST',
     data: json_data,
     success: function(d) {
       console.log("успех", d);
       teach_list = $.evalJSON(d)
       modal_add.fill_teach(teach_list)
     },
     error: function(d) {
       console.log("не успех", d);
     }
   });
});


$('#korpus').change(function(event) {
  var json_data = {"name":$('#korpus option:selected').text()}
  $.ajax({
     url: '/get_room',
     method: 'POST',
     data: json_data,
     success: function(d) {
        console.log("успех", d);
        room_list = $.evalJSON(d)
        modal_add.fill_room(room_list)
     },
     error: function(d) {
       console.log("не успех", d);
     }
   });
});



function data_from_data(lesson){
  teach = teach_list[data["teach-lesson"]]
  name = lesson_list[data["name-lesson"]]
  korpus = korpus_list[data["korpus-lesson"]]
  room = room_list[data["room-lesson"]]
  type = type_list[data["type-lesson"]]
  lesson.new_data(name, teach, korpus, room, type)
}

$('#modal_save').click( function () {
  if (modal_add.validate()) {
    number_v = ("l" +  (parseInt(modal_add.number)))
    current_lesson = timetable[modal_add.week][modal_add.day][number_v]
    data_from_data(current_lesson)
    modal_add.hide()
    str = current_lesson.fill_lesson()
    current_cell.empty()
    current_cell.append(str)
  }
});


$('#modal_delete').click( function () {
    number_v = ("l" +  (parseInt(modal_add.number)));
    current_lesson = timetable[modal_add.week][modal_add.day][number_v];

    timetable[modal_add.week][modal_add.day][number_v] = new Lesson();
    modal_add.hide();
    // str = current_lesson.fill_lesson()
    current_cell.empty()
    // current_cell.append(str)
});

class Lesson {

  new_data (name, teach, korpus, room, type) {
    this.name = name
    this.teach = teach
    this.korpus = korpus
    this.room = room
    this.type = type
  }

  fill_lesson (element) {
    const lesson_temp =
        `
        <div class="d-flex flex-column">  
            <div class="cell-style cell-lesson-name">${this.name}</div>
            <div class="cell-style cell-lesson-teach">${this.teach}</div>
        </div>
        <div class="d-flex  flex-row" >  
            <div class="cell-lesson-room col-6">${this.korpus}-${this.room}</div>   
            <div class="cell-lesson-type col-6">${this.type}</div>
        </div>
        `
    return lesson_temp
  }
}


class Day {
  constructor () {
    this.l1 =  new Lesson()
    this.l2 =  new Lesson()
    this.l3 =  new Lesson()
    this.l4 =  new Lesson()
    this.l5 =  new Lesson()
    this.l6 =  new Lesson()
  }
}


class Week {
  constructor(){
      this.mon =  new Day()
      this.tues =  new Day()
      this.wen =  new Day()
      this.thurs=  new Day()
      this.fri =  new Day()
      this.sat =  new Day()
  }
}

class TimeTable {
  constructor (id) {
    this.first = new Week()
    this.second = new Week()
    this.id = id
  }

  save_changes_ajax() {
  var json_data = $.toJSON($(this))
  $.ajax({
     url: '/save_changes',
     method: 'POST',
     data: json_data,
     success: function(d) {
       console.log("успех", d);
     },
     error: function(d) {
       console.log("не успех", d);
     }
   });
  }
}



// var new_json = json_d.replace("&quot;", "\"")
$('#modal_reset_all').click( function () {
    if (confirm("Это действие невозможно будет отменить !")){
        timetable = new TimeTable(group_id)
        timetable.save_changes_ajax()
        window.location.href =  ""
    }


});


var timetable = new TimeTable(group_id)
var tt
console.log(json_d)
var new_json = json_d.split('&#39;').join('\"');
console.log(new_json)

if (new_json)
{
  tt = $.evalJSON(new_json)
}
// var lesson_list = $.evalJSON(new_stroka)

for (var key in tt) {
  week = tt[key]
  weekTarget = timetable[key]
  // console.log("weeeeeeeeeeeeeek", week)
  for (var key2 in week){

    days = week[key2]
    dayTarget = weekTarget[key2]
    // console.log("daaaaaaaays", days)

    for (var key3 in days){
      lesson = days[key3]
      if (lesson.name != undefined){
        timetable[key][key2][key3].name = lesson.name
        timetable[key][key2][key3].teach = lesson.teach
        timetable[key][key2][key3].korpus = lesson.korpus
        timetable[key][key2][key3].room = lesson.room
        timetable[key][key2][key3].type = lesson.type
        console.log("leeeessssooon", timetable[key][key2][key3])
        targetLesson = timetable[key][key2][key3]
        s = `.${key} .${key2} .${key3}`

        s2 = targetLesson.fill_lesson()
        $(s).append(s2)
        }

      // console.log("=======", timetable)
    }
  }
}
console.log("=======", timetable)
