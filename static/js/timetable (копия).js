
var number
var day
var week
var teach_list = {0:"Выберете преподавателя", 1:"Рыбанов А.А", 2:"Короткова Н.Н", 3:"Абрамова О.Ф.", 4:"Саньков С.Г"}
var lesson_list = {0:"Выберете предмет", 1:"Базы данных", 2:"Исследовние операций", 3:"Компьютерная грамотность", 4:"Операционые системы"}
var room_list = {0:"Выберете аудиторию", 1:"В-201", 2:"В-202", 3:"В-206", 4:"А-21"}
var type_list = {0:"Выберете тип занятия", 1:"Лекция", 2:"Практика", 3:"Лаб."}
var week_c = {"first" : "Первая неделя", "second": "Вторая неделя"}
var day_c = {mon : "Понедельник",
             tues: "Вторник",
             wen: "Среда",
             thurs: "Четверг",
             fri: "Пятница",
             sat: "Суббота"
            }


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
      $('#room').empty()
      $('#type').empty()

      $.each(lesson_list, function(key,  value) {
        $('#name').append('<option value="' + key + '">' + value + '</option>');

      });
      $.each(teach_list, function(key,  value) {
        $('#teach').append('<option value="' + key + '">' + value + '</option>');

      });
      $.each(room_list, function(key,  value) {
        $('#room').append('<option value="' + key + '">' + value + '</option>');

      });
      $.each(type_list, function(key,  value) {
        $('#type').append('<option value="' + key + '">' + value + '</option>');

      });
    }

    fill_info () {
            $(".week_modal").empty()
            $(".week_modal").append(`<strong>${week_c[this.week]}</strong>`)

            $(".day_modal").empty()
            $(".day_modal").append(`<i>${day_c[this.day]}, ${this.number} пара</i>`)

            $('#modal_error').empty()
    }

    show() {
        this.fill_info()
        $("#addLesson").modal('show');
    }

    hide() {
      $("#addLesson").modal('hide');
      // this.generateModal()
      this.save_changes_ajax()
    }



    save_changes_ajax() {
      var json_data = $.toJSON(timetable)
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

function data_from_data(lesson){
  teach = teach_list[data["teach-lesson"]]
  name = lesson_list[data["name-lesson"]]
  room = room_list[data["room-lesson"]]
  type = type_list[data["type-lesson"]]
  lesson.new_data(name, teach, room, type)
}

$('#modal_save').click( function () {
  if (modal_add.validate()) {
    current_lesson = timetable["week"][modal_add.week]["days"][modal_add.day]["lessons"][modal_add.number-1]
    data_from_data(current_lesson)
    modal_add.hide()
    str = current_lesson.fill_lesson()
    current_cell.empty()
    current_cell.append(str)
  }
});

class Lesson {


  constructor () {

  }

  new_data (name, teach, room, type) {
    this.name = name
    this.teach = teach
    this.room = room
    this.type = type
  }

  fill_lesson (element) {
    const lesson_temp = `<div class="cell-style cell-lesson-name">${this.name}</div>
    <div class="cell-style cell-lesson-teach">${this.teach}</div>
    <div class="d-flex flex-row">  <div class="cell-lesson-room col-6">${this.room}</div>   <div class="cell-lesson-type col-6">${this.type}</div>   </div>`
    return lesson_temp
  }

  


}

class Day {
  constructor () {
    this.lessons = [ new Lesson(), new Lesson(), new Lesson(), new Lesson(), new Lesson(), new Lesson() ]
  }

}

class Week {
  constructor(){
    this.days = {
      mon: new Day(),
      tues: new Day(),
      wen: new Day(),
      thurs: new Day(),
      fri: new Day(),
      sat: new Day(),
    }
  }
}

class TimeTable {
  constructor () {
    this.week = {
      first: new Week(),
      second: new Week()
    }
  }

}

// var new_json = json_d.replace("&quot;", "\"")


var timetable = new TimeTable()
var tt
console.log(json_d)
var new_json = json_d.split('&quot;').join('\"');
console.log(new_json)
if (new_json) 
{
  tt = $.evalJSON(new_json)
}
for (let key in tt) {

  weeks = tt[key];
  weeksTarget = timetable[key];
  for (let key in weeks) {
    week = weeks[key];
    weekTarget = weeksTarget[key]
    //console.log(week, key);
    // first second
    
    for (let key in week) {
      days = week[key];
      daysTarget = weekTarget[key]
      //console.log(days, key);
      // days

      for (let key in days) {
        day = days[key];
        dayTarget = daysTarget[key]
        // all days

        for (let key in day) {
          lessons = day[key]
          lessonsTarget = dayTarget[key]

          for (let key in lessons) {
            lesson = lessons[key]
            lessonTarget = lessonsTarget[key]
            // lessons num
            console.log(lesson);
            for (let key in lesson) {
              shtuka = lesson[key];
              lessonTarget[key]=shtuka;
              console.log(shtuka);
           }
          }
        }
      }
    }
  } 
}


console.log("=====". tt)