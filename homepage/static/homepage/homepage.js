// homepage app JS //

document.addEventListener('DOMContentLoaded', function() {

    if (document.getElementById('msg')){
      setTimeout(function() {
        document.getElementById('msg').style.visibility ='hidden'
      }, 3000);      
    }
    if(document.getElementById('eatDrinkVisit')){
        const eat_link = document.getElementById('navLinkEat')
        const drink_link = document.getElementById('navLinkDrink')
        const visit_link = document.getElementById('navLinkVisit')
      
        // EAT LINK change bg-image on mouse over 
        eat_link.addEventListener("mouseenter", function() {
          document.querySelector("main").classList.toggle("eat-bg")
        }); 
        // and togle back to origina when mouse leave
        eat_link.addEventListener("mouseleave", function() {
          document.querySelector("main").classList.toggle("eat-bg")
        });  
        // DRINK LINK change bg-image on mouse over 
        drink_link.addEventListener("mouseenter", function() {
          document.querySelector("main").classList.toggle("drink-bg")
        }); 
        // and togle back to origina when mouse leave
        drink_link.addEventListener("mouseleave", function() {
          document.querySelector("main").classList.toggle("drink-bg")
        });  
        // VISIT LINK change bg-image on mouse over 
        visit_link.addEventListener("mouseenter", function() {
          document.querySelector("main").classList.toggle("visit-bg")
        }); 
        // and togle back to origina when mouse leave
        visit_link.addEventListener("mouseleave", function() {
          document.querySelector("main").classList.toggle("visit-bg")
        });       
    }
    if( document.getElementById('eatPage')){
      console.log('estPage')
      accordion_eat()
    }
    if( document.getElementById('drinkPage')){
      console.log('drinkPage')
      accordion();
    }
});

function accordion() {
  const acc_tabs = document.querySelectorAll('.acc-tab')

  var tab_content=''

  var first_tab_content = acc_tabs[0].nextElementSibling
  first_tab_content.style.display = 'block'
  acc_tabs.forEach((tab) => {
    tab.onclick = function(event) {
      tab_clicked = event.target
      console.log(tab_clicked)
      tab_content_id = tab_clicked.innerText.replace(/\s/g, '')
      console.log(tab_content_id)
      tab_content = document.getElementById(tab_content_id)
      console.log(tab_content)
      if(tab_content.style.display == 'block'){
        tab_content.style.display = 'none'
      }
      else
      {
        tab_content.style.display = 'block'
      }
    }
  })
  console.log(acc_tabs[0])
}

function accordion_eat() {
  const eat_tabs = document.querySelectorAll('.accordion-tab-eat')

  var tab_content=''

  var first_tab_content = eat_tabs[0].nextElementSibling
  first_tab_content.style.display = 'block'

  eat_tabs.forEach((tab) => {
    tab.onclick = function(event) {
      tab_clicked = event.target
      // console.log(tab_clicked)
      tab_content_id = tab_clicked.innerText.replace(/\s/g, '')
      // console.log(tab_content_id)
      tab_content = document.getElementById(tab_content_id)
      // console.log(tab_content)
      if(tab_content.style.display == 'block'){
        tab_content.style.display = 'none'
      }
      else
      {
        tab_content.style.display = 'block'
      }
    }
  })

}

function reservation()
{
    const rform = document.getElementById('reservationForm');

    rform.onsubmit = function(){

      fields = rform.elements
      let day = ''
      let hour = ''
      let pax =''

      if(document.querySelector('input[name="days"]:checked')){
        day = document.querySelector('input[name="days"]:checked').value
      }
      if(document.querySelector('input[name="hours"]:checked')){
        hour = document.querySelector('input[name="hours"]:checked').value
      }
      if(document.querySelector('input[name="pax"]:checked'))
      {
        pax = document.querySelector('input[name="pax"]:checked').value
      }
        
      // console.log('const', day, hour, pax)      
      if(day == '' || hour == '' || pax =='') 
      {
        document.getElementById('reservationMessages').innerHTML = `form incomplete check DAY, HOUR, PERSONS`
        // console.log('incomplete')
        return false
      }
      else {
        rform.submit()
      }
      return false;
    }
}
