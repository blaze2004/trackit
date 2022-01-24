window.addEventListener('scroll', function() {
    let header = document.querySelector('header');
    let windowlPosition = window.scrollY > 0;
    header.classList.toggle('scrolling-active', windowlPosition);
});

function save_data() {
    let data = localStorage.getItem('latest_meet_attendance');

    if (data != null) {
        var save_request = new XMLHttpRequest();
        save_request.open("POST", "http://127.0.0.1:8000/mac/save_attendance/", true);
        save_request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        save_request.onreadystatechange = function() {
            if (save_request.readyState == 4 && save_request.status == 200) {
                console.log('Attendance saved to database.');
                localStorage.clear();
            } else {
                console.log('Server Error!');
            }
        }
        save_request.send('latest_meet_attendance=' + data);
    }
}

window.addEventListener('load', save_data);