$(document).ready(function() {
    $('#menu_toggle').on('click', function () {
      $('.surah_list').toggleClass("hidden");

    });
});


document.addEventListener("DOMContentLoaded", function (event) {
    var scrollpos = sessionStorage.getItem('scrollpos');

    if (scrollpos) {
        window.scrollTo(0, scrollpos);
        sessionStorage.removeItem('scrollpos');
    }
});

window.addEventListener("scroll", function (e) {
  
  sessionStorage.setItem('scrollpos', window.scrollY);

});

  