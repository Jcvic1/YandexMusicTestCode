setTimeout(function () {
  $(".alert")
    .fadeTo(500, 0)
    .slideUp(500, function () {
      $(this).remove();
    });
}, 3500);

setTimeout(function () {
  $("#sm-screenFull")
    .fadeTo(500, 0)
    .slideDown(500, function () {
      $(this).remove();
    });
}, 3500);


function toggleYaMusic() {
  var x = document.getElementById("yandex_search");
  var y = document.getElementById("yandex_player");
  if (x.style.display === "none" && y.style.display === "block") {
    x.style.display = "block";
    y.style.display = "none";
  } else {
    x.style.display = "none";
    y.style.display = "block";
  }
}



function peopleSearch() {
  var searchProfiles = document.querySelectorAll(".search-profile");
 searchProfiles.forEach(searchProfile => {
  if (searchProfile.style.display === "none") {
    searchProfile.style.display = "block";
  } else {
    searchProfile.style.display = "none";
  }
});
}

setTimeout(function () {
  $(".drop_down")
    .fadeTo(500, 0)
    .slideUp(500, function () {
      $(this).remove();
    });
}, 5000);



function toggleYaMusicFull() {
var ym = document.getElementById("yandex_full");
var icon = document.getElementById("icon");
var bottom = document.getElementById("bottom");
var bg = document.getElementById("bg");

  ym.classList.toggle("fullscreen");
  if (icon.classList.contains("bi-arrows-angle-expand")) {
    icon.classList.remove("bi-arrows-angle-expand");
    icon.classList.add("bi-arrows-angle-contract");
  } else {
    icon.classList.remove("bi-arrows-angle-contract");
    icon.classList.add("bi-arrows-angle-expand");
  }
  if (bottom.classList.contains("sticky-bottom")) {
    bottom.classList.remove("sticky-bottom");
    bottom.classList.add("fixed-bottom");
  } else {
    bottom.classList.remove("fixed-bottom");
    bottom.classList.add("sticky-bottom");
  }
  
}



function toggleYaMusicFullPeople() {
  var ym_people = document.getElementById("yandex_full_people");
  var icon_people = document.getElementById("icon_people");
  var bottom_people = document.getElementById("bottom_people");
  var bg = document.getElementById("bg_people");
  
    ym_people.classList.toggle("fullscreen");
    if (icon_people.classList.contains("bi-arrows-angle-expand")) {
      icon_people.classList.remove("bi-arrows-angle-expand");
      icon_people.classList.add("bi-arrows-angle-contract");
    } else {
      icon_people.classList.remove("bi-arrows-angle-contract");
      icon_people.classList.add("bi-arrows-angle-expand");
    }
    if (bottom_people.classList.contains("sticky-bottom")) {
      bottom_people.classList.remove("sticky-bottom");
      bottom_people.classList.add("fixed-bottom");
    } else {
      bottom_people.classList.remove("fixed-bottom");
      bottom_people.classList.add("sticky-bottom");
    }
    if (bg_people.classList.contains("bg-dark")) {
      bg_people.classList.remove("bg-dark");
    } else {
      bg_people.classList.add("bg-dark");
    }
  }



  function toggleYaMusicFullProfile() {
    var ym_profile = document.getElementById("yandex_full_profile");
    var icon_profile = document.getElementById("icon_profile");
    var bottom_profile = document.getElementById("bottom_profile");
    var bg_profile = document.getElementById("bg_profile");
    
      ym_profile.classList.toggle("fullscreen");
      if (icon_profile.classList.contains("bi-arrows-angle-expand")) {
        icon_profile.classList.remove("bi-arrows-angle-expand");
        icon_profile.classList.add("bi-arrows-angle-contract");
      } else {
        icon_profile.classList.remove("bi-arrows-angle-contract");
        icon_profile.classList.add("bi-arrows-angle-expand");
      }
      if (bottom_profile.classList.contains("sticky-bottom")) {
        bottom_profile.classList.remove("sticky-bottom");
        bottom_profile.classList.add("fixed-bottom");
      } else {
        bottom_profile.classList.remove("fixed-bottom");
        bottom_profile.classList.add("sticky-bottom");
      }
      if (bg_profile.classList.contains("bg-dark")) {
        bg_profile.classList.remove("bg-dark");
      } else {
        bg_profile.classList.add("bg-dark");
      }
    }

    