$('.owl-carousel').owlCarousel({
    loop: true,
    dots: true,
    nav: true,
    responsiveClass: true,
    pullDrag: true,
    touchDrag: true,
    autoplay: false,
    autoplayTimeout: 2000,
    smartSpeed: 400,
    autoplayHoverPause: true,
    lazyLoad: true,

    responsive: {
        0: {
            margin: 20,
            items: 1,
            nav: true,
            smartSpeed: 200,
            autoplay: false
        },
        600: {
            margin: 200,
            items: 3,
            nav: false
        },
        1000: {
            margin: 200,
            items: 4,
            nav: true,
            loop: false
        }
    }
})
window.onscroll = function () { myFunction() };

var header = document.getElementById("myHeader");
var sticky = header.offsetTop;

function myFunction() {
    if (window.pageYOffset >= sticky) {
        header.classList.add("fixed-top");
    } else {
        header.classList.remove("fixed-top");
    }
}


function filterInsturment(insturment){
    var all, b;
    allElement = document.getElementsByClassName("filterInsturment");
    if(instrument=="all") {
        instrument = "filterInsturment";

    }

    for(i = 0; i < allElement.length;i++){
        if(allElement[i].classList.contains(instrument)){

            if(!allElement[i].parentNode.classList.contains("activetag")){
                allElement[i].parentNode.classList.add("activetag");
            }
            if(allElement[i].parentNode.classList.contains("lazytag")){
                allElement[i].parentNode.classList.remove("lazytag");
            }
        }
        else{
            if(!allElement[i].parentNode.classList.contains("lazytag")){
                allElement[i].parentNode.classList.add("lazytag");
            }
            if(allElement[i].parentNode.classList.contains("activetag")){
                allElement[i].parentNode.classList.remove("activetag");
            }
        }
    }
}



$(function() {

      var today = moment().startOf('day').format('YYYY-MM-DD');
      $('#studentSchedule').fullCalendar({
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
        header: {
            left: 'title',
            right : 'month,agendaWeek,agendaDay',
          center: 'prev,today,next '


        },

        handleWindowResize: true,
        longPressDelay: true,

        eventLongPressDelay: true,
        selectLongPressDelay: true,
        eventLimit: true,
        events: [

                {% for class in lessons %}

                {

                    title:  "{{ class.instrument }}" + ' Lesson',
                    start:  "{{ class.class_time|date:"Y-m-d H:i:s" }}",
                    className: 'bg-greenblue',
                    description: "{{ class.get_instrument_display }}" + ' lesson with ' + "{{ class.teacher.user.first_name }} {{ class.teacher.user.last_name }}",
                },

                {% endfor %}



            // other events here...
          ],
          timeFormat: 'H(:mm)' ,// uppercase H for 24-hour clock
          eventClick:  function(event, jsEvent, view) {
            $('#eventTitle').html(event.title);
            $('#eventBody').html(event.eventBody);
            $('#scheduleModal').modal();
            $('#description').html(event.description);
            $('#eventTime').html(moment(event.start).format('MMM Do h:mm A'));
        }

      });

});


$('.load-btn').on('click', function() {
    var $this = $(this);
    var loadingText = "<i class='fa fa-spinner fa-spin  mr-1'></i> Processing";
    if ($(this).html() !== loadingText) {
        $this.data('original-text',  $(this).html());
        $this.html(loadingText);
      }
    setTimeout(function() {


    if(true){ //Any condition
        $this.html("<i class='fas fa-check mr-1'></i> Hire Success");
        $this.removeClass("btn-info");
        $this.addClass("btn-success");
    }
    else{
        $this.html("<i class='fas fa-times mr-1'></i> Hire Failed");
        $this.removeClass("btn-info");
        $this.addClass("btn-danger");
    }

    }, 1600);


});

